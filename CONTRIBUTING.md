# Contributing to Stock Trading Dashboard

Thank you for your interest in contributing to the Stock Trading Dashboard! This document provides guidelines and instructions for contributing.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Process](#development-process)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Submitting Changes](#submitting-changes)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)

## Code of Conduct

This project follows a Code of Conduct that we expect all contributors to adhere to. Please be respectful, professional, and inclusive in all interactions.

### Our Standards

- **Be Respectful**: Treat everyone with respect and consideration
- **Be Collaborative**: Work together to resolve conflicts constructively
- **Be Professional**: Focus on what is best for the community
- **Be Inclusive**: Welcome newcomers and help them get started

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Basic understanding of Python and financial markets
- Familiarity with APIs and web scraping

### Setting Up Your Development Environment

1. **Fork the Repository**
   ```bash
   # Click the 'Fork' button on GitHub
   ```

2. **Clone Your Fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/stock-trading-dashboard.git
   cd stock-trading-dashboard
   ```

3. **Add Upstream Remote**
   ```bash
   git remote add upstream https://github.com/ORIGINAL_OWNER/stock-trading-dashboard.git
   ```

4. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

5. **Install Development Dependencies**
   ```bash
   make setup-dev
   # Or manually:
   pip install -r requirements.txt
   ```

6. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API credentials
   ```

## Development Process

### Branching Strategy

We use Git Flow branching model:

- `main` - Production-ready code
- `develop` - Integration branch for features
- `feature/*` - New features
- `bugfix/*` - Bug fixes
- `hotfix/*` - Emergency fixes for production

### Creating a Feature Branch

```bash
# Update your develop branch
git checkout develop
git pull upstream develop

# Create feature branch
git checkout -b feature/your-feature-name
```

### Making Changes

1. **Write Code**
   - Follow our coding standards
   - Keep changes focused and atomic
   - Write clear, descriptive commit messages

2. **Test Your Changes**
   ```bash
   make test
   make coverage
   ```

3. **Format Your Code**
   ```bash
   make format
   ```

4. **Lint Your Code**
   ```bash
   make lint
   ```

### Commit Messages

Follow the Conventional Commits specification:

```
type(scope): subject

body

footer
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```bash
feat(scraper): add StockTwits integration

Implemented scraping functionality for StockTwits platform
to aggregate additional stock mentions.

Closes #123
```

```bash
fix(analyzer): correct P/E ratio calculation

Fixed division by zero error when earnings data is unavailable.

Fixes #456
```

## Coding Standards

### Python Style Guide

We follow PEP 8 with some modifications:

- **Line Length**: Maximum 120 characters
- **Indentation**: 4 spaces (no tabs)
- **Imports**: Organized with isort
- **Quotes**: Single quotes for strings
- **Docstrings**: Google style

### Code Structure

```python
"""
Module docstring describing the module's purpose.
"""

import standard_library
import third_party_library
from local_module import LocalClass

# Constants
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30

class ClassName:
    """
    Class docstring.
    
    Attributes:
        attribute_name (type): Description
    """
    
    def __init__(self, param: str):
        """
        Initialize the class.
        
        Args:
            param (str): Description of parameter
        """
        self.attribute = param
    
    def method_name(self, arg: int) -> bool:
        """
        Method docstring.
        
        Args:
            arg (int): Description of argument
            
        Returns:
            bool: Description of return value
            
        Raises:
            ValueError: Description of when this is raised
        """
        pass
```

### Docstring Format

Use Google-style docstrings:

```python
def function_name(param1: str, param2: int = 0) -> dict:
    """
    Brief description of function.
    
    Longer description if needed. Can span multiple lines
    and include more detailed information about the function.
    
    Args:
        param1 (str): Description of first parameter
        param2 (int, optional): Description of optional parameter. Defaults to 0.
    
    Returns:
        dict: Description of return value with structure:
            {
                'key1': value description,
                'key2': value description
            }
    
    Raises:
        TypeError: When param1 is not a string
        ValueError: When param2 is negative
    
    Examples:
        >>> function_name('test', 5)
        {'result': 'success'}
    """
    pass
```

## Testing Guidelines

### Writing Tests

- Write tests for all new features
- Maintain test coverage above 80%
- Use descriptive test names
- Follow AAA pattern (Arrange, Act, Assert)

### Test Structure

```python
import unittest
from src.module import ClassName

class TestClassName(unittest.TestCase):
    """Test cases for ClassName."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.instance = ClassName()
    
    def tearDown(self):
        """Clean up after tests."""
        pass
    
    def test_method_with_valid_input(self):
        """Test method with valid input."""
        # Arrange
        input_data = 'test'
        expected = 'result'
        
        # Act
        result = self.instance.method(input_data)
        
        # Assert
        self.assertEqual(result, expected)
    
    def test_method_with_invalid_input(self):
        """Test method raises error with invalid input."""
        with self.assertRaises(ValueError):
            self.instance.method(None)
```

### Running Tests

```bash
# Run all tests
make test

# Run specific test file
pytest tests/test_scraper.py -v

# Run with coverage
make coverage

# Run and watch for changes
pytest-watch
```

## Submitting Changes

### Before Submitting

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] Code coverage maintained/improved
- [ ] Documentation updated
- [ ] Commit messages follow convention
- [ ] Branch is up to date with develop

### Pull Request Process

1. **Update Your Branch**
   ```bash
   git checkout develop
   git pull upstream develop
   git checkout feature/your-feature
   git rebase develop
   ```

2. **Push Your Changes**
   ```bash
   git push origin feature/your-feature
   ```

3. **Create Pull Request**
   - Go to GitHub and create a PR
   - Use the PR template
   - Link related issues
   - Request reviews

4. **PR Template**
   ```markdown
   ## Description
   Brief description of changes
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update
   
   ## Testing
   Describe testing performed
   
   ## Checklist
   - [ ] Code follows style guidelines
   - [ ] Tests added/updated
   - [ ] Documentation updated
   - [ ] No new warnings
   
   ## Related Issues
   Closes #123
   ```

5. **Address Review Comments**
   - Respond to all comments
   - Make requested changes
   - Push updates to same branch

6. **Merge**
   - Maintainer will merge when approved
   - Delete your branch after merge

## Reporting Bugs

### Before Submitting a Bug Report

1. **Check existing issues** - Your bug might already be reported
2. **Update to latest version** - Bug might be fixed
3. **Verify it's a bug** - Not expected behavior

### Bug Report Template

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
- OS: [e.g., Windows 10]
- Python version: [e.g., 3.9.7]
- Package version: [e.g., 1.0.0]

**Additional context**
Any other relevant information.
```

## Suggesting Enhancements

### Enhancement Proposal Template

```markdown
**Is your feature request related to a problem?**
Clear description of the problem.

**Describe the solution you'd like**
Clear description of what you want to happen.

**Describe alternatives you've considered**
Alternative solutions or features you've considered.

**Additional context**
Any other context or screenshots.

**Possible Implementation**
If you have ideas on how to implement this.
```

## Development Tips

### Useful Commands

```bash
# Format code
make format

# Check code style
make lint

# Run tests
make test

# Generate coverage report
make coverage

# Clean build artifacts
make clean

# Start the application
make run
```

### Debugging

```python
# Use logging instead of print
import logging
logger = logging.getLogger(__name__)

logger.debug("Debug information")
logger.info("Informational message")
logger.warning("Warning message")
logger.error("Error message")
```

### Performance Considerations

- Use caching when appropriate
- Minimize API calls
- Profile code for bottlenecks
- Consider asynchronous operations

## Questions?

- Create an issue with the question label
- Join our community discussions
- Check existing documentation

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing! 🎉