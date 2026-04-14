# Contributing to API Unifier

Thank you for your interest in contributing to API Unifier! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Bug Reports](#bug-reports)
- [Feature Requests](#feature-requests)
- [Style Guidelines](#style-guidelines)
- [Community](#community)

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Basic understanding of REST, GraphQL, and SOAP APIs

### Quick Start

1. Fork the repository
2. Clone your fork locally
3. Create a new branch for your feature
4. Make your changes
5. Submit a pull request

## How to Contribute

We welcome contributions in several areas:

### Bug Fixes
- Fix reported issues
- Improve error handling
- Edge case handling

### Features
- New API type support
- Authentication methods
- Response normalization improvements
- Performance optimizations

### Documentation
- Improve README
- Add examples
- Fix typos
- Translate documentation

### Testing
- Add unit tests
- Improve test coverage
- Add integration tests

## Development Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/mrsuicidefox/api-unifier.git
   cd api-unifier
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

4. **Install development dependencies**:
   ```bash
   pip install pytest pytest-cov black flake8 mypy
   ```

## Testing

### Run Tests
```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=api_unifier --cov-report=html

# Run specific test file
python -m pytest test_api_unifier.py
```

### Test Structure
- Unit tests are in `test_api_unifier.py`
- Use mocking for external API calls
- Test all authentication methods
- Test error conditions

### Writing Tests
```python
import unittest
from unittest.mock import Mock, patch
from api_unifier import UniversalAPI

class YourTest(unittest.TestCase):
    def setUp(self):
        self.api = UniversalAPI('https://api.example.com', 'rest')
    
    @patch('requests.Session.get')
    def test_your_feature(self, mock_get):
        # Your test code here
        pass
```

## Submitting Changes

### Branch Naming
- `fix/issue-description` for bug fixes
- `feature/feature-description` for new features
- `docs/documentation-change` for documentation

### Commit Messages
Use clear and descriptive commit messages:
```
type(scope): description

Examples:
feat(auth): add OAuth2 authentication support
fix(soap): handle empty SOAP responses properly
docs(readme): update installation instructions
```

### Pull Request Process

1. **Update README.md** if you've changed the API
2. **Add tests** for new functionality
3. **Ensure all tests pass**
4. **Update documentation** if needed
5. **Submit pull request** with:
   - Clear title and description
   - Link to related issues
   - Screenshots if applicable

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] Added new tests
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
```

## Bug Reports

### Before Reporting
- Check existing issues
- Search for similar problems
- Verify it's not a configuration issue

### Bug Report Template

```markdown
**Bug Description**
Clear description of the bug

**Steps to Reproduce**
1. Go to...
2. Click on...
3. See error

**Expected Behavior**
What you expected to happen

**Actual Behavior**
What actually happened

**Environment**
- OS: [e.g. Windows 11, macOS 13.0]
- Python version: [e.g. 3.10.0]
- API Unifier version: [e.g. 1.0.0]

**Additional Context**
Add any other context about the problem
```

## Feature Requests

### Feature Request Template

```markdown
**Feature Description**
Clear description of the feature

**Problem Statement**
What problem does this solve?

**Proposed Solution**
How you envision this feature working

**Alternatives Considered**
Other approaches you've thought about

**Additional Context**
Any other relevant information
```

## Style Guidelines

### Code Style
- Follow PEP 8
- Use Black for formatting
- Maximum line length: 88 characters
- Use type hints where appropriate

### Documentation Style
- Use clear, concise language
- Include code examples
- Document all public methods
- Use consistent formatting

### Example Code Style
```python
def example_function(param1: str, param2: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Brief description of what this function does.
    
    Args:
        param1: Description of param1
        param2: Optional description of param2
    
    Returns:
        Dictionary containing the result
    
    Raises:
        ValueError: If param1 is invalid
    """
    if not param1:
        raise ValueError("param1 cannot be empty")
    
    # Your implementation here
    return {"result": "success"}
```

## Development Guidelines

### API Design Principles
- Keep the interface consistent across API types
- Maintain backward compatibility
- Use meaningful error messages
- Document all public methods

### Performance Considerations
- Minimize external dependencies
- Optimize for common use cases
- Consider memory usage
- Add performance tests for critical paths

### Security Considerations
- Never log sensitive information
- Validate all inputs
- Use secure defaults
- Follow security best practices

## Community

### Getting Help
- Open an issue for questions
- Join discussions in GitHub Discussions
- Check the documentation first

### Recognition
- Contributors will be listed in the README
- Major contributors may get maintainer access
- Your name will appear in commit history

## Release Process

### Version Bumping
- Follow semantic versioning
- Update version in setup.py
- Update changelog
- Create GitHub release

### Changelog Format
```markdown
## [1.1.0] - 2024-01-15

### Added
- New feature description

### Fixed
- Bug fix description

### Changed
- Breaking change description

### Deprecated
- Feature that will be removed
```

## Questions?

If you have questions about contributing:

1. Check existing issues and discussions
2. Read the documentation thoroughly
3. Open an issue with your question
4. Tag maintainers if needed

---

Thank you for contributing to API Unifier! Your contributions help make this project better for everyone.
