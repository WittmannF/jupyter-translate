import json, os, re, sys
import argparse
from deep_translator import (
    GoogleTranslator,
    MyMemoryTranslator
)
from tqdm import tqdm  # For progress bar
from time import sleep

# Função para selecionar o tradutor com base no nome
def get_translator(translator_name, src_language, dest_language):
    translators = {
        'google': GoogleTranslator,
        'mymemory': MyMemoryTranslator,
    }
    TranslatorClass = translators.get(translator_name.lower())
    if not TranslatorClass:
        raise ValueError(f"Translator {translator_name} not supported.")
    
    try:
        print(f"Using translator: {translator_name.capitalize()}")
        print(f"Source language: {src_language}, Target language: {dest_language}")
        
        # Get supported languages
        supported_languages = TranslatorClass().get_supported_languages(as_dict=True)
        
        # Check if source and target languages are supported
        if src_language not in supported_languages.values():
            print(f"Warning: Source language '{src_language}' might not be supported. Available languages:")
            for code, lang in supported_languages.items():
                if src_language.lower() in lang.lower():
                    print(f"  - Did you mean '{lang}' (code: {code})?")
        
        if dest_language not in supported_languages.values():
            print(f"Warning: Target language '{dest_language}' might not be supported. Available languages:")
            for code, lang in supported_languages.items():
                if dest_language.lower() in lang.lower():
                    print(f"  - Did you mean '{lang}' (code: {code})?")
        
        # Initialize translator with source and target languages
        return TranslatorClass(source=src_language, target=dest_language)
        
    except Exception as e:
        if 'No support for the provided language' in str(e):
            print(f"Error: {e}")
            supported_languages = TranslatorClass().get_supported_languages(as_dict=True)
            print(f"Supported languages for {translator_name}: {supported_languages}")
        else:
            print(f"Error initializing the translator: {e}")
        sys.exit(1)

def safe_translate(translator, text, retries=3, delay=10):
    if not text.strip():  # Skip empty texts
        return text
        
    print(f"Translating text: {text[:30]}...")  # Debug: Show what we're translating
    for i in range(retries):
        try:
            translated = translator.translate(text)
            print(f"Translation result: {translated[:30]}...")  # Debug: Show result
            return translated
        except Exception as e:
            print(f"Error translating: {str(e)}. Trying again ({i+1}/{retries})...")
            sleep(delay)
    raise Exception(f"Failed to translate after {retries} attempts.")

def translate_markdown(text, translator, delay):
    # Regex expressions
    MD_CODE_REGEX = r'```[a-z]*\n[\s\S]*?\n```'
    CODE_REPLACEMENT_KW = r'xx_markdown_code_xx'
    
    MD_LINK_REGEX = r'\[([^\]]+)\]\(([^)]+)\)'
    LINK_REPLACEMENT_KW = 'xx_markdown_link_xx'

    # Markdown tags
    END_LINE = '\n'
    IMG_PREFIX = '!['
    HEADERS = ['### ', '###', '## ', '##', '# ', '#']  # Should be from this order (bigger to smaller)

    print(f"Processing markdown text: {text[:30]}...")  # Debug

    # Inner function to replace tags from text from a source list
    def replace_from_list(tag, text, replacement_list):
        if not replacement_list:
            return text
        replacement_list = list(replacement_list)  # Ensure it's a list
        replacement_iter = iter(replacement_list)
        
        def replace_match(match):
            nonlocal replacement_iter
            try:
                return next(replacement_iter)
            except StopIteration:
                # Reset iterator if we ran out of replacements
                replacement_iter = iter(replacement_list)
                return next(replacement_iter)
                
        return re.sub(tag, replace_match, text)

    # Inner function for translation
    def translate(text):
        # Get all markdown links
        md_links = re.findall(MD_LINK_REGEX, text)
        print(f"Found {len(md_links)} markdown links")  # Debug

        # Get all markdown code blocks
        md_codes = re.findall(MD_CODE_REGEX, text)
        print(f"Found {len(md_codes)} markdown code blocks")  # Debug

        # Replace markdown links in text to markdown_link
        text = re.sub(MD_LINK_REGEX, LINK_REPLACEMENT_KW, text)

        # Replace links in markdown to tag markdown_link
        text = re.sub(MD_CODE_REGEX, CODE_REPLACEMENT_KW, text)

        print(f"Text after replacements (before translation): {text[:50]}...")  # Debug

        # Translate text
        text = safe_translate(translator, text, delay=delay)

        print(f"Text after translation: {text[:50]}...")  # Debug

        # Replace tags to original link tags
        if md_links:
            # Reconstruct the original markdown links
            original_links = [f"[{title}]({url})" for title, url in md_links]
            text = replace_from_list(LINK_REPLACEMENT_KW, text, original_links)

        # Replace code tags
        if md_codes:
            text = replace_from_list(CODE_REPLACEMENT_KW, text, md_codes)

        return text

    # Check if there are special Markdown tags
    if len(text) >= 2:
        if text[-1:] == END_LINE:
            return translate(text) + '\n'

        if text[:2] == IMG_PREFIX:
            return text

        for header in HEADERS:
            len_header = len(header)
            if text[:len_header] == header:
                return header + translate(text[len_header:])

    return translate(text)

def translate_code_comments_and_prints(code, translator, delay):
    if not code or code.isspace():
        return code

    def translate_text(text):
        return safe_translate(translator, text, delay=delay)

    # Split line by line to handle multi-line code
    lines = code.split('\n')
    translated_lines = []
    
    for line in lines:
        # Handle comments (# ... )
        if '#' in line:
            code_part, comment_part = line.split('#', 1)
            translated_comment = translate_text(comment_part.strip())
            translated_line = f"{code_part}# {translated_comment}"
            translated_lines.append(translated_line)
            continue
            
        # Skip f-string print statements entirely to preserve variable references
        if 'print(f' in line:
            translated_lines.append(line)  # Keep f-string prints unchanged
            continue
            
        # Handle regular print statements
        if 'print(' in line and ('f"' not in line and "f'" not in line):
            # Try to match regular print statements
            match = re.search(r'print\(\s*["\'](.+?)["\']\s*(?:,.*?)?\)', line)
            if match:
                text_to_translate = match.group(1)
                translated_text = translate_text(text_to_translate)
                # Replace the original text with translated text
                translated_line = line.replace(text_to_translate, translated_text)
                translated_lines.append(translated_line)
                continue
        
        # If none of the above conditions match, keep the line as is
        translated_lines.append(line)
    
    return '\n'.join(translated_lines)

def jupyter_translate(fname, src_language, dest_language, delay, translator_name, rename_source_file=False, print_translation=False):
    """
    Translates a Jupyter Notebook from one language to another.
    """

    # Initialize the translator
    translator = get_translator(translator_name, src_language, dest_language)
    
    # Test the translator with a simple text
    test_text = "Teste de tradução. Isso deve ser traduzido."
    try:
        test_result = translator.translate(test_text)
        print(f"Translator test - Original: '{test_text}' → Translated: '{test_result}'")
    except Exception as e:
        print(f"Translator test failed: {str(e)}")
        print("The translator is not working correctly. Please check your settings and try again.")
        sys.exit(1)

    # Check if the necessary parameters are provided
    if not fname or not dest_language:
        print("Error: Missing required parameters.")
        print("Usage: python jupyter_translate.py <notebook_file> --source <source_language> --target <destination_language> --translator <translator>")
        sys.exit(1)

    # Load the notebook file
    with open(fname, 'r', encoding='utf-8') as file:
        data_translated = json.load(file)

    total_cells = len(data_translated['cells'])
    code_cells = sum(1 for cell in data_translated['cells'] if cell['cell_type'] == 'code')
    markdown_cells = sum(1 for cell in data_translated['cells'] if cell['cell_type'] == 'markdown')

    print(f"Total cells: {total_cells}")
    print(f"Code cells: {code_cells}")
    print(f"Markdown cells: {markdown_cells}")

    # Translate each cell
    for i, cell in enumerate(tqdm(data_translated['cells'], desc="Translating cells", unit="cell")):
        if cell['cell_type'] == 'markdown':
            # For markdown cells, we need to handle special markdown syntax
            # Join all source lines into a single string for better translation
            full_markdown = ''.join(cell['source'])
            
            # Translate the whole markdown content
            translated_markdown = translate_markdown(full_markdown, translator, delay=delay)
            
            # Split the translated content back into lines
            data_translated['cells'][i]['source'] = translated_markdown.splitlines(True)  # keepends=True to preserve newlines
            
            if print_translation:
                print(f"Translated markdown cell {i}:")
                print(''.join(data_translated['cells'][i]['source']))
                
        elif cell['cell_type'] == 'code':
            # For code cells, translate comments and print statements
            translated_source = []
            for source_line in cell['source']:
                # Translate comments and formatted print statements within code
                translated_line = translate_code_comments_and_prints(source_line, translator, delay=delay)
                translated_source.append(translated_line)
                
            data_translated['cells'][i]['source'] = translated_source
            
            if print_translation:
                print(f"Translated code cell {i}:")
                print(''.join(data_translated['cells'][i]['source']))

    if rename_source_file:
        fname_bk = f"{'.'.join(fname.split('.')[:-1])}_bk.ipynb"  # index.ipynb -> index_bk.ipynb

        os.rename(fname, fname_bk)
        print(f'{fname} has been renamed as {fname_bk}')

        with open(fname, 'w', encoding='utf-8') as f:
            json.dump(data_translated, f, ensure_ascii=False, indent=2)
        print(f'The {dest_language} translation has been saved as {fname}')
    else:
        dest_fname = f"{'.'.join(fname.split('.')[:-1])}_{dest_language}.ipynb"  # any.name.ipynb -> any.name_en.ipynb
        with open(dest_fname, 'w', encoding='utf-8') as f:
            json.dump(data_translated, f, ensure_ascii=False, indent=2)
        print(f'The {dest_language} translation has been saved as {dest_fname}')

# Main function to parse arguments and run the translation
def main():
    parser = argparse.ArgumentParser(description="Translate a Jupyter Notebook from one language to another.")
    parser.add_argument('fname', help="Path to the Jupyter Notebook file")
    parser.add_argument('--source', default='auto', help="Source language code (default: auto-detect)")
    parser.add_argument('--target', required=True, help="Destination language code")
    parser.add_argument('--delay', type=int, default=10, help="Delay between retries in seconds (default: 10)")
    parser.add_argument('--translator', default='google', help="Translator to use (options: google or mymemory). Default: google")
    parser.add_argument('--rename', action='store_true', help="Rename the original file after translation")
    parser.add_argument('--print', dest='print_translation', action='store_true', help="Print translations to console")

    args = parser.parse_args()

    # Map common language names to ISO codes if full names are provided
    language_map = {
        'english': 'en',
        'portuguese': 'pt',
        'spanish': 'es',
        'french': 'fr',
        'german': 'de',
        'italian': 'it',
        'dutch': 'nl',
        'chinese': 'zh-CN',
        'japanese': 'ja',
        'korean': 'ko',
        'russian': 'ru',
        'arabic': 'ar'
    }

    # Convert source and target languages to ISO codes if they are full names
    src_language = args.source.lower()
    if src_language in language_map:
        src_language = language_map[src_language]
    
    dest_language = args.target.lower()
    if dest_language in language_map:
        dest_language = language_map[dest_language]

    print(f"Using source language code: {src_language}, target language code: {dest_language}")

    jupyter_translate(
        fname=args.fname,
        src_language=src_language,
        dest_language=dest_language,
        delay=args.delay,
        translator_name=args.translator,
        rename_source_file=args.rename,
        print_translation=args.print_translation
    )

if __name__ == '__main__':
    main()


