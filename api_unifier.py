#!/usr/bin/env python3
"""
API Unifier - Make all APIs work the same way
Universal API wrapper for REST, GraphQL, and SOAP services
"""

import requests
import json
import xml.etree.ElementTree as ET
from typing import Dict, Any, Optional, Union
from urllib.parse import urljoin, urlparse
import base64


class UniversalAPI:
    """
    Universal API wrapper that normalizes different API types
    REST, GraphQL, and SOAP all work the same way
    """
    
    def __init__(self, base_url: str, api_type: str = "rest", auth: Optional[Dict] = None):
        """
        Initialize Universal API
        
        Args:
            base_url: Base URL for the API
            api_type: Type of API ('rest', 'graphql', 'soap')
            auth: Authentication dict {'type': 'bearer/basic/api_key', 'token': 'token'}
        """
        self.base_url = base_url.rstrip('/')
        self.api_type = api_type.lower()
        self.auth = auth
        self.session = requests.Session()
        
        # Setup authentication
        if auth:
            self._setup_auth()
    
    def _setup_auth(self):
        """Setup authentication based on type"""
        auth_type = self.auth.get('type', '').lower()
        token = self.auth.get('token', '')
        
        if auth_type == 'bearer':
            self.session.headers.update({'Authorization': f'Bearer {token}'})
        elif auth_type == 'basic':
            credentials = base64.b64encode(f"{token}".encode()).decode()
            self.session.headers.update({'Authorization': f'Basic {credentials}'})
        elif auth_type == 'api_key':
            key_name = self.auth.get('key_name', 'X-API-Key')
            self.session.headers.update({key_name: token})
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Universal GET request"""
        if self.api_type == 'rest':
            return self._rest_get(endpoint, params)
        elif self.api_type == 'graphql':
            return self._graphql_query(endpoint, params)
        elif self.api_type == 'soap':
            return self._soap_request(endpoint, 'GET', params)
    
    def post(self, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Universal POST request"""
        if self.api_type == 'rest':
            return self._rest_post(endpoint, data)
        elif self.api_type == 'graphql':
            return self._graphql_mutation(endpoint, data)
        elif self.api_type == 'soap':
            return self._soap_request(endpoint, 'POST', data)
    
    def put(self, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Universal PUT request"""
        if self.api_type == 'rest':
            return self._rest_put(endpoint, data)
        elif self.api_type == 'soap':
            return self._soap_request(endpoint, 'PUT', data)
    
    def delete(self, endpoint: str) -> Dict[str, Any]:
        """Universal DELETE request"""
        if self.api_type == 'rest':
            return self._rest_delete(endpoint)
        elif self.api_type == 'soap':
            return self._soap_request(endpoint, 'DELETE')
    
    # REST Methods
    def _rest_get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """REST GET request"""
        url = urljoin(self.base_url, endpoint)
        response = self.session.get(url, params=params)
        return self._normalize_response(response)
    
    def _rest_post(self, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """REST POST request"""
        url = urljoin(self.base_url, endpoint)
        response = self.session.post(url, json=data)
        return self._normalize_response(response)
    
    def _rest_put(self, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """REST PUT request"""
        url = urljoin(self.base_url, endpoint)
        response = self.session.put(url, json=data)
        return self._normalize_response(response)
    
    def _rest_delete(self, endpoint: str) -> Dict[str, Any]:
        """REST DELETE request"""
        url = urljoin(self.base_url, endpoint)
        response = self.session.delete(url)
        return self._normalize_response(response)
    
    # GraphQL Methods
    def _graphql_query(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """GraphQL query"""
        url = urljoin(self.base_url, endpoint)
        
        if isinstance(params, str):
            query = params
        else:
            query = self._dict_to_graphql_query(params)
        
        response = self.session.post(url, json={'query': query})
        return self._normalize_response(response)
    
    def _graphql_mutation(self, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """GraphQL mutation"""
        url = urljoin(self.base_url, endpoint)
        mutation = self._dict_to_graphql_mutation(data)
        
        response = self.session.post(url, json={'query': mutation})
        return self._normalize_response(response)
    
    def _dict_to_graphql_query(self, params: Dict) -> str:
        """Convert dict to GraphQL query"""
        if not params:
            return "{ }"
        
        fields = ", ".join(params.keys())
        return f"{{ {fields} }}"
    
    def _dict_to_graphql_mutation(self, data: Dict) -> str:
        """Convert dict to GraphQL mutation"""
        if not data:
            return "mutation { }"
        
        # Simple mutation generation
        mutation_name = list(data.keys())[0]
        mutation_data = data[mutation_name]
        
        return f"mutation {{ {mutation_name}({mutation_data}) }}"
    
    # SOAP Methods
    def _soap_request(self, endpoint: str, method: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """SOAP request"""
        url = urljoin(self.base_url, endpoint)
        
        # Create SOAP envelope
        soap_envelope = self._create_soap_envelope(method, data)
        
        headers = {'Content-Type': 'text/xml; charset=utf-8'}
        response = self.session.post(url, data=soap_envelope, headers=headers)
        
        return self._normalize_soap_response(response)
    
    def _create_soap_envelope(self, method: str, data: Optional[Dict]) -> str:
        """Create SOAP envelope"""
        soap_data = ""
        if data:
            for key, value in data.items():
                soap_data += f"<{key}>{value}</{key}>"
        
        envelope = f"""<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <{method}>
      {soap_data}
    </{method}>
  </soap:Body>
</soap:Envelope>"""
        return envelope
    
    def _normalize_soap_response(self, response: requests.Response) -> Dict[str, Any]:
        """Normalize SOAP response to dict"""
        try:
            root = ET.fromstring(response.text)
            
            # Extract data from SOAP response
            result = {}
            for child in root.iter():
                if child.text and child.text.strip():
                    result[child.tag] = child.text.strip()
            
            return {
                'success': response.status_code == 200,
                'status_code': response.status_code,
                'data': result,
                'raw_response': response.text
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'SOAP parsing error: {str(e)}',
                'raw_response': response.text
            }
    
    def _normalize_response(self, response: requests.Response) -> Dict[str, Any]:
        """Normalize any API response to standard format"""
        try:
            # Try to parse JSON
            if response.headers.get('content-type', '').startswith('application/json'):
                data = response.json()
            else:
                # Fallback to text
                data = response.text
            
            return {
                'success': 200 <= response.status_code < 300,
                'status_code': response.status_code,
                'data': data,
                'headers': dict(response.headers),
                'url': response.url
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Response parsing error: {str(e)}',
                'status_code': response.status_code,
                'raw_response': response.text
            }


class APIRegistry:
    """
    Registry for managing multiple APIs with the same interface
    """
    
    def __init__(self):
        self.apis = {}
    
    def register(self, name: str, api: UniversalAPI):
        """Register an API with a name"""
        self.apis[name] = api
    
    def get(self, name: str) -> UniversalAPI:
        """Get an API by name"""
        if name not in self.apis:
            raise ValueError(f"API '{name}' not registered")
        return self.apis[name]
    
    def call_all(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Call the same method on all registered APIs"""
        results = {}
        
        for name, api in self.apis.items():
            try:
                if method.lower() == 'get':
                    results[name] = api.get(endpoint, data)
                elif method.lower() == 'post':
                    results[name] = api.post(endpoint, data)
                elif method.lower() == 'put':
                    results[name] = api.put(endpoint, data)
                elif method.lower() == 'delete':
                    results[name] = api.delete(endpoint)
            except Exception as e:
                results[name] = {'success': False, 'error': str(e)}
        
        return results


# Convenience functions for quick setup
def rest_api(base_url: str, auth: Optional[Dict] = None) -> UniversalAPI:
    """Quick setup for REST API"""
    return UniversalAPI(base_url, 'rest', auth)


def graphql_api(base_url: str, auth: Optional[Dict] = None) -> UniversalAPI:
    """Quick setup for GraphQL API"""
    return UniversalAPI(base_url, 'graphql', auth)


def soap_api(base_url: str, auth: Optional[Dict] = None) -> UniversalAPI:
    """Quick setup for SOAP API"""
    return UniversalAPI(base_url, 'soap', auth)


# Example usage
if __name__ == "__main__":
    # REST API example
    github_api = rest_api('https://api.github.com', {
        'type': 'bearer',
        'token': 'your_token_here'
    })
    
    # GraphQL API example
    graphql_api = graphql_api('https://api.github.com/graphql', {
        'type': 'bearer',
        'token': 'your_token_here'
    })
    
    # Multiple API management
    registry = APIRegistry()
    registry.register('github_rest', github_api)
    registry.register('github_graphql', graphql_api)
    
    print("API Unifier ready!")
    print("Use the same interface for REST, GraphQL, and SOAP APIs!")
