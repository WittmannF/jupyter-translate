import pytest
import sys
import os

# Add the parent directory to the path so we can import jupyter_translate in all tests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture(autouse=True)
def disable_network_calls(monkeypatch):
    """
    Fixture to disable actual network calls during tests.
    This ensures tests don't make actual API calls to translation services.
    """
    def mock_sleep(*args, **kwargs):
        pass
    
    # Patch sleep function to speed up tests
    monkeypatch.setattr('time.sleep', mock_sleep) 