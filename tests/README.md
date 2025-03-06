# Tests for Jupyter Translate

This directory contains tests for the Jupyter Translate package.

## Running Tests

To run all tests:
```
pytest
```

To run with coverage:
```
pytest --cov=jupyter_translate
```

To run specific test file:
```
pytest tests/test_unit.py
pytest tests/test_integration.py
```

## Structure

- `test_unit.py`: Unit tests for individual functions in the jupyter_translate module
- `test_integration.py`: Integration tests for the complete workflow
- `conftest.py`: Shared fixtures and setup for tests 