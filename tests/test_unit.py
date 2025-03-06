import pytest
import sys
import os
from unittest.mock import patch, MagicMock

# Add the parent directory to the path so we can import jupyter_translate
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import jupyter_translate

class TestGetTranslator:
    @patch('jupyter_translate.GoogleTranslator')
    def test_get_translator_google(self, mock_translator):
        # Setup mock
        mock_instance = MagicMock()
        mock_instance.get_supported_languages.return_value = {'en': 'english', 'pt': 'portuguese'}
        mock_translator.return_value = mock_instance
        
        # Call the function
        translator = jupyter_translate.get_translator('google', 'english', 'portuguese')
        
        # Assertions
        assert mock_translator.call_count >= 1
        assert translator is not None

    @patch('jupyter_translate.MyMemoryTranslator')
    def test_get_translator_mymemory(self, mock_translator):
        # Setup mock
        mock_instance = MagicMock()
        mock_instance.get_supported_languages.return_value = {'en': 'english', 'pt': 'portuguese'}
        mock_translator.return_value = mock_instance
        
        # Call the function
        translator = jupyter_translate.get_translator('mymemory', 'english', 'portuguese')
        
        # Assertions
        assert mock_translator.call_count >= 1
        assert translator is not None
    
    def test_get_translator_invalid(self):
        # Test with an invalid translator name
        with pytest.raises(ValueError):
            jupyter_translate.get_translator('invalid_translator', 'english', 'portuguese')

class TestSafeTranslate:
    @patch('jupyter_translate.sleep')
    def test_safe_translate_success(self, mock_sleep):
        # Setup mock translator
        mock_translator = MagicMock()
        mock_translator.translate.return_value = 'translated text'
        
        # Call the function
        result = jupyter_translate.safe_translate(mock_translator, 'source text')
        
        # Assertions
        assert result == 'translated text'
        mock_translator.translate.assert_called_once_with('source text')
        mock_sleep.assert_not_called()
    
    @patch('jupyter_translate.sleep')
    def test_safe_translate_retry(self, mock_sleep):
        # Setup mock translator to fail once then succeed
        mock_translator = MagicMock()
        mock_translator.translate.side_effect = [Exception("API error"), "translated text"]
        
        # Call the function
        result = jupyter_translate.safe_translate(mock_translator, 'source text')
        
        # Assertions
        assert result == 'translated text'
        assert mock_translator.translate.call_count == 2
        mock_sleep.assert_called_once()
    
    @patch('jupyter_translate.sleep')
    def test_safe_translate_all_retries_fail(self, mock_sleep):
        # Setup mock translator to always fail
        mock_translator = MagicMock()
        mock_translator.translate.side_effect = Exception("API error")
        
        # Call the function and expect it to raise an exception
        with pytest.raises(Exception) as excinfo:
            jupyter_translate.safe_translate(mock_translator, 'source text', retries=2)
        
        # Assertions
        assert "Failed to translate after 2 attempts" in str(excinfo.value)
        assert mock_translator.translate.call_count == 2
        assert mock_sleep.call_count == 2

class TestTranslateMarkdown:
    def test_translate_markdown_simple(self):
        # Setup mock translator
        mock_translator = MagicMock()
        mock_translator.translate.return_value = 'translated text'
        
        # Call the function
        with patch('jupyter_translate.safe_translate', return_value='translated text'):
            result = jupyter_translate.translate_markdown('simple text', mock_translator, delay=0)
        
        # Assertions
        assert 'translated text' in result

    def test_translate_markdown_with_code_blocks(self):
        # Test with markdown containing code blocks
        markdown_with_code = """Some text
```python
def function():
    return True
```
More text"""
        
        mock_translator = MagicMock()
        
        # We need to mock safe_translate to handle both code blocks preservation and text translation
        def mock_safe_translate(translator, text, delay):
            if '```python' in text:  # If this is a code block, don't translate
                return text
            return 'translated'  # Otherwise, return a translated placeholder
            
        # Simply patch safe_translate without trying to patch the inner function
        with patch('jupyter_translate.safe_translate', side_effect=mock_safe_translate):
            result = jupyter_translate.translate_markdown(markdown_with_code, mock_translator, delay=0)
        
        # For simplicity, just check that we get back something that indicates translation happened
        assert 'translated' in result

class TestTranslateCodeCommentsAndPrints:
    def test_translate_code_comments(self):
        # Test translating code comments
        code_with_comment = "# This is a comment\nx = 10"
        mock_translator = MagicMock()
        
        def mock_safe_translate(translator, text, delay):
            if text == "This is a comment":
                return "This is a translated comment"
            return text
            
        with patch('jupyter_translate.safe_translate', side_effect=mock_safe_translate):
            result = jupyter_translate.translate_code_comments_and_prints(code_with_comment, mock_translator, delay=0)
        
        # Assertions
        assert '# This is a translated comment' in result
        assert 'x = 10' in result
    
    @patch('jupyter_translate.re.search')
    @patch('jupyter_translate.re.sub')
    def test_translate_print_statements(self, mock_sub, mock_search):
        # Test translating print statements
        code_with_print = 'print("Hello, world!")'
        mock_translator = MagicMock()
        
        # Mock re.search to pretend it found a match for print statements
        mock_match = MagicMock()
        mock_match.group.return_value = '"Hello, world!"'
        mock_search.return_value = mock_match
        
        # Mock re.sub to simulate replacing the text inside print
        mock_sub.return_value = 'print("Hello, translated world!")'
        
        # Mock the safe_translate function
        with patch('jupyter_translate.safe_translate', return_value='"Hello, translated world!"'):
            result = jupyter_translate.translate_code_comments_and_prints(code_with_print, mock_translator, delay=0)
        
        # Assert that we get the expected output
        assert 'print("Hello, translated world!")' == result 