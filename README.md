# 🚀 API Unifier

**Make all APIs work the same way** - Universal wrapper for REST, GraphQL, and SOAP services

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Stars](https://img.shields.io/github/stars/yourusername/api-unifier?style=social)](https://github.com/yourusername/api-unifier)

## ✨ Why This Exists

Tired of learning different API formats for every service?
- **REST APIs** with different response structures
- **GraphQL** with complex queries  
- **SOAP** with XML envelopes
- **Different authentication** methods

**API Unifier makes them all work the same way.**

## 🎯 One Interface for Everything

```python
# REST API
api = UniversalAPI('https://api.github.com', 'rest', auth)
result = api.get('/user')  # Same for all APIs!

# GraphQL API  
api = UniversalAPI('https://api.github.com/graphql', 'graphql', auth)
result = api.get('/user')  # Same interface!

# SOAP API
api = UniversalAPI('https://example.com/soap', 'soap', auth)
result = api.get('/user')  # Still the same!
```

## 🚀 Quick Start

### Installation
```bash
pip install api-unifier
```

### Basic Usage
```python
from api_unifier import UniversalAPI, rest_api, graphql_api

# Quick setup functions
github = rest_api('https://api.github.com', {
    'type': 'bearer',
    'token': 'your_token'
})

# Same interface for everything
user = github.get('/user')
repos = github.get('/user/repos')

# Create new repo
new_repo = github.post('/user/repos', {
    'name': 'my-new-repo',
    'private': False
})
```

## 🔥 Features

### 🌐 Multi-Protocol Support
- **REST APIs** - Full CRUD operations
- **GraphQL** - Queries and mutations
- **SOAP** - XML-based services

### 🔐 Universal Authentication
```python
# Bearer Token
auth = {'type': 'bearer', 'token': 'your_token'}

# API Key
auth = {'type': 'api_key', 'token': 'your_key', 'key_name': 'X-API-Key'}

# Basic Auth
auth = {'type': 'basic', 'token': 'username:password'}
```

### 📊 Normalized Responses
All APIs return the same format:
```python
{
    'success': True,
    'status_code': 200,
    'data': {...},
    'headers': {...},
    'url': '...'
}
```

### 🏪 API Registry
Manage multiple APIs easily:
```python
from api_unifier import APIRegistry

registry = APIRegistry()
registry.register('github', github_api)
registry.register('twitter', twitter_api)

# Call all APIs at once
results = registry.call_all('get', '/user')
```

## 📚 Examples

### GitHub API (REST)
```python
github = rest_api('https://api.github.com', {
    'type': 'bearer',
    'token': 'ghp_your_token'
})

# Get user info
user = github.get('/user')
print(user['data']['login'])

# Create repository
repo = github.post('/user/repos', {
    'name': 'awesome-project',
    'description': 'Built with API Unifier!'
})
```

### Shopify API (GraphQL)
```python
shopify = graphql_api('https://your-shop.myshopify.com/api/graphql', {
    'type': 'bearer',
    'token': 'shpat_your_token'
})

# Get products
query = """
{
  products(first: 10) {
    edges {
      node {
        title
        priceRangeV2 {
          minVariantPrice {
            amount
          }
        }
      }
    }
  }
}
"""

products = shopify.get('', query)
```

### Weather API (SOAP)
```python
weather = soap_api('https://example.com/weather/api')

# Get weather data
weather_data = weather.get('/getCurrentWeather', {
    'city': 'New York',
    'units': 'metric'
})
```

### Multiple API Calls
```python
# Setup multiple APIs
apis = APIRegistry()
apis.register('github', github_api)
apis.register('twitter', twitter_api)
apis.register('linkedin', linkedin_api)

# Get user data from all platforms
user_data = apis.call_all('get', '/user/me')

# Post to all platforms
post_result = apis.call_all('post', '/posts', {
    'content': 'Hello from API Unifier!'
})
```

## 🎪 Real-World Use Cases

### 📊 Data Aggregation
```python
# Collect user data from multiple platforms
def get_user_profile(username):
    apis = setup_social_apis(username)
    
    profile_data = {
        'github': apis.get('github').get(f'/users/{username}'),
        'twitter': apis.get('twitter').get(f'/users/{username}'),
        'linkedin': apis.get('linkedin').get(f'/people/{username}')
    }
    
    return normalize_profile_data(profile_data)
```

### 🔄 API Migration
```python
# Migrate from REST to GraphQL without changing code
old_rest_api = rest_api('https://api.example.com/v1')
new_graphql_api = graphql_api('https://api.example.com/graphql')

# Same interface, different backend
def get_user_data(user_id):
    try:
        return new_graphql_api.get(f'/user/{user_id}')
    except:
        return old_rest_api.get(f'/users/{user_id}')
```

### 🧪 API Testing
```python
# Test same endpoint across different API versions
def test_api_compatibility(base_url):
    v1 = UniversalAPI(f'{base_url}/v1', 'rest')
    v2 = UniversalAPI(f'{base_url}/v2', 'rest')
    v3 = UniversalAPI(f'{base_url}/v3', 'graphql')
    
    results = {
        'v1_rest': v1.get('/user'),
        'v2_rest': v2.get('/user'), 
        'v3_graphql': v3.get('/user')
    }
    
    return compare_api_responses(results)
```

## 🛠️ Advanced Usage

### Custom Headers
```python
api = UniversalAPI('https://api.example.com', 'rest')
api.session.headers.update({
    'User-Agent': 'MyApp/1.0',
    'Accept': 'application/vnd.api+json'
})
```

### Error Handling
```python
result = api.get('/endpoint')

if not result['success']:
    print(f"Error: {result.get('error', 'Unknown error')}")
    print(f"Status code: {result['status_code']}")
else:
    data = result['data']
    # Process successful response
```

### Rate Limiting
```python
import time
from api_unifier import UniversalAPI

class RateLimitedAPI(UniversalAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_call = 0
    
    def get(self, endpoint, params=None):
        # Wait if calling too fast
        if time.time() - self.last_call < 1.0:
            time.sleep(1.0)
        
        result = super().get(endpoint, params)
        self.last_call = time.time()
        return result
```

## 🏆 Best For

1. **Solves Real Pain** - Every developer deals with API fragmentation
2. **Dead Simple** - One interface for everything
3. **Zero Dependencies** - Uses only `requests`
4. **Perfect Documentation** - Clear examples for everything
5. **Universal Solution** - Works with any API type

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if possible
5. Submit a pull request

## 📄 License

MIT License - feel free to use this in your projects!

## 💝 Support This Project

**Love API Unifier?** Help keep it maintained and growing!

### 🪙 Cryptocurrency Donations
- **Bitcoin (BTC)**: bc1q9l7jwd5dunq5xyuu4prxa3lhttrdzv6n3yma4c
- **Ethereum (ETH)**: 0x80F432A8Ab4Dc4A9e25EB1EB4d94D575DF2654FF 
- **USDT (TRC20)**: TPr5ZTdZEaHUMuKnSvXSupMYkEPWhPfNqW
- **Solana (SOL)**: 
- **KASPA (KAS)**:
kaspa:qppu3nnkj856gg5emw3t2wqms4w9vpsxc7lxtvdzfknjgm4xej9kqk6v45q4y


### 🌟 Free Ways to Support
- ⭐ [Star the repository](https://github.com/mrsuicidefox/api-unifier)
- 🐦 [Share on Twitter](https://twitter.com/intent/tweet?text=Check%20out%20API%20Unifier%20-%20Make%20all%20APIs%20work%20the%20same%20way!%20https://github.com/mrsuicidefox/api-unifier)
- 📝 [Contribute to the project](https://github.com/mrsuicidefox/api-unifier/blob/main/CONTRIBUTING.md)

## 🌟 Show Some Love

If this project helped you, please:

- ⭐ Star the repository
- 🐦 Tweet about it
- 💬 Share with your network
- 🤝 Contribute back

---

**Made with ❤️ by developers who hate API fragmentation**

[![GitHub stars](https://img.shields.io/github/stars/mrsuicidefox/api-unifier?style=social)](https://github.com/mrsuicidefox/api-unifier)
[![GitHub forks](https://img.shields.io/github/forks/mrsuicidefox/api-unifier?style=social)](https://github.com/mrsuicidefox/api-unifier)
[![GitHub issues](https://img.shields.io/github/issues/mrsuicidefox/api-unifier)](https://github.com/mrsuicidefox/api-unifier/issues)
