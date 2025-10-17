# Test Documentation

This directory contains comprehensive tests for the Mergington High School Activities API.

## Test Structure

- `conftest.py` - Test configuration, fixtures, and setup
- `test_main.py` - Tests for main application endpoints
- `test_signup.py` - Tests for student signup functionality
- `test_unregister.py` - Tests for student unregister functionality

## Running Tests

To run all tests:
```bash
python -m pytest tests/ -v
```

To run tests with coverage report:
```bash
python -m pytest tests/ --cov=src --cov-report=term-missing
```

To run a specific test file:
```bash
python -m pytest tests/test_signup.py -v
```

## Test Coverage

The test suite provides 100% code coverage for the main application logic, including:

- ✅ Root endpoint redirection
- ✅ Activities listing endpoint
- ✅ Student signup functionality
- ✅ Student unregister functionality  
- ✅ Error handling for invalid requests
- ✅ URL encoding/decoding support
- ✅ Duplicate signup prevention
- ✅ Data validation and structure

## Test Features

### Fixtures
- `client` - FastAPI test client for making HTTP requests
- `reset_activities` - Resets activity data to initial state before each test
- `sample_email` - Provides a test email address
- `sample_activity` - Provides a test activity name

### Test Categories
- **Happy Path Tests** - Normal usage scenarios
- **Error Handling Tests** - Invalid inputs and edge cases
- **URL Encoding Tests** - Special characters in URLs
- **Workflow Tests** - Complete signup/unregister flows
- **Data Validation Tests** - Proper data structure validation