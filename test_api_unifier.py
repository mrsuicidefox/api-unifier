#!/usr/bin/env python3
"""
Test suite for API Unifier
"""

import unittest
from unittest.mock import Mock, patch
from api_unifier import UniversalAPI, APIRegistry, rest_api, graphql_api, soap_api


class TestUniversalAPI(unittest.TestCase):
    """Test UniversalAPI functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.api = UniversalAPI('https://api.example.com', 'rest')
    
    def test_init(self):
        """Test API initialization"""
        self.assertEqual(self.api.base_url, 'https://api.example.com')
        self.assertEqual(self.api.api_type, 'rest')
        self.assertIsNotNone(self.api.session)
    
    def test_bearer_auth_setup(self):
        """Test Bearer token authentication"""
        api = UniversalAPI('https://api.example.com', 'rest', {
            'type': 'bearer',
            'token': 'test_token'
        })
        self.assertIn('Authorization', api.session.headers)
        self.assertEqual(api.session.headers['Authorization'], 'Bearer test_token')
    
    def test_api_key_auth_setup(self):
        """Test API key authentication"""
        api = UniversalAPI('https://api.example.com', 'rest', {
            'type': 'api_key',
            'token': 'test_key',
            'key_name': 'X-Custom-Key'
        })
        self.assertIn('X-Custom-Key', api.session.headers)
        self.assertEqual(api.session.headers['X-Custom-Key'], 'test_key')
    
    def test_basic_auth_setup(self):
        """Test Basic authentication"""
        api = UniversalAPI('https://api.example.com', 'rest', {
            'type': 'basic',
            'token': 'username:password'
        })
        self.assertIn('Authorization', api.session.headers)
        self.assertTrue(api.session.headers['Authorization'].startswith('Basic '))
    
    @patch('requests.Session.get')
    def test_rest_get_success(self, mock_get):
        """Test successful REST GET request"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'data': 'test'}
        mock_response.headers = {'content-type': 'application/json'}
        mock_response.url = 'https://api.example.com/test'
        mock_get.return_value = mock_response
        
        result = self.api.get('/test')
        
        self.assertTrue(result['success'])
        self.assertEqual(result['status_code'], 200)
        self.assertEqual(result['data'], {'data': 'test'})
    
    @patch('requests.Session.get')
    def test_rest_get_error(self, mock_get):
        """Test REST GET request with error"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {'error': 'Not found'}
        mock_response.headers = {'content-type': 'application/json'}
        mock_response.url = 'https://api.example.com/test'
        mock_get.return_value = mock_response
        
        result = self.api.get('/test')
        
        self.assertFalse(result['success'])
        self.assertEqual(result['status_code'], 404)
    
    @patch('requests.Session.post')
    def test_rest_post_success(self, mock_post):
        """Test successful REST POST request"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {'id': 1, 'data': 'created'}
        mock_response.headers = {'content-type': 'application/json'}
        mock_response.url = 'https://api.example.com/test'
        mock_post.return_value = mock_response
        
        result = self.api.post('/test', {'data': 'test'})
        
        self.assertTrue(result['success'])
        self.assertEqual(result['status_code'], 201)
        self.assertEqual(result['data'], {'id': 1, 'data': 'created'})
    
    def test_graphql_query_from_string(self):
        """Test GraphQL query from string"""
        api = UniversalAPI('https://api.example.com', 'graphql')
        
        with patch('requests.Session.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {'data': {'user': {'name': 'test'}}}
            mock_response.headers = {'content-type': 'application/json'}
            mock_response.url = 'https://api.example.com/graphql'
            mock_post.return_value = mock_response
            
            query = "{ user { name } }"
            result = api.get('', query)
            
            self.assertTrue(result['success'])
            mock_post.assert_called_once()
    
    def test_dict_to_graphql_query(self):
        """Test dict to GraphQL query conversion"""
        api = UniversalAPI('https://api.example.com', 'graphql')
        query = api._dict_to_graphql_query({'user': 'name', 'posts': 'title'})
        self.assertEqual(query, '{ user, posts }')
    
    def test_dict_to_graphql_mutation(self):
        """Test dict to GraphQL mutation conversion"""
        api = UniversalAPI('https://api.example.com', 'graphql')
        mutation = api._dict_to_graphql_mutation({'createUser': 'name: "test"'})
        self.assertEqual(mutation, 'mutation { createUser(name: "test") }')
    
    def test_soap_envelope_creation(self):
        """Test SOAP envelope creation"""
        api = UniversalAPI('https://api.example.com', 'soap')
        envelope = api._create_soap_envelope('testMethod', {'param1': 'value1'})
        
        self.assertIn('<soap:Envelope', envelope)
        self.assertIn('<testMethod>', envelope)
        self.assertIn('<param1>value1</param1>', envelope)
        self.assertIn('</soap:Envelope>', envelope)


class TestAPIRegistry(unittest.TestCase):
    """Test API Registry functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.registry = APIRegistry()
        self.api = UniversalAPI('https://api.example.com', 'rest')
    
    def test_register_api(self):
        """Test API registration"""
        self.registry.register('test_api', self.api)
        self.assertIn('test_api', self.registry.apis)
        self.assertEqual(self.registry.apis['test_api'], self.api)
    
    def test_get_api(self):
        """Test getting registered API"""
        self.registry.register('test_api', self.api)
        retrieved_api = self.registry.get('test_api')
        self.assertEqual(retrieved_api, self.api)
    
    def test_get_nonexistent_api(self):
        """Test getting non-existent API raises error"""
        with self.assertRaises(ValueError):
            self.registry.get('nonexistent_api')
    
    @patch.object(UniversalAPI, 'get')
    def test_call_all_get(self, mock_get):
        """Test calling GET on all registered APIs"""
        mock_get.return_value = {'success': True, 'data': 'test'}
        
        api2 = UniversalAPI('https://api2.example.com', 'rest')
        self.registry.register('api1', self.api)
        self.registry.register('api2', api2)
        
        results = self.registry.call_all('get', '/test')
        
        self.assertIn('api1', results)
        self.assertIn('api2', results)
        self.assertEqual(len(results), 2)


class TestConvenienceFunctions(unittest.TestCase):
    """Test convenience functions"""
    
    def test_rest_api_function(self):
        """Test rest_api convenience function"""
        api = rest_api('https://api.example.com')
        self.assertEqual(api.base_url, 'https://api.example.com')
        self.assertEqual(api.api_type, 'rest')
    
    def test_graphql_api_function(self):
        """Test graphql_api convenience function"""
        api = graphql_api('https://api.example.com')
        self.assertEqual(api.base_url, 'https://api.example.com')
        self.assertEqual(api.api_type, 'graphql')
    
    def test_soap_api_function(self):
        """Test soap_api convenience function"""
        api = soap_api('https://api.example.com')
        self.assertEqual(api.base_url, 'https://api.example.com')
        self.assertEqual(api.api_type, 'soap')


if __name__ == '__main__':
    unittest.main()
