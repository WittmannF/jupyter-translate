"""
History:
- 08 Aug 2024: Introduced argparse for handling command-line arguments, including options for specifying input (--source) and output (--target) languages, as well as the file path.
- 09 Aug 2024: Transitioned from googletrans to deep-translator for improved translation stability and compatibility.
- 09 Aug 2024: Added error handling for missing required parameters (--source and --target).
- 12 Aug 2024: modified version to have default --source as en, and introduce "attempts" with sleep (default delay is 15 sec), to prevent overflow of the deep-translator API
- 12 Aug 2024: Added option for different translators using --translator and print the default (googletrans)
"""
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
        return TranslatorClass(source=src_language, target=dest_language)
    except Exception as e:
        if 'No support for the provided language' in str(e):
            print(f"Erro: {e}")
            supported_languages = TranslatorClass().get_supported_languages(as_dict=True)
            print(f"Supported languages {translator_name}: {supported_languages}")
        else:
            print(f"Error initializing the translator: {e}")
        sys.exit(1)

def safe_translate(translator, text, retries=3, delay=10):
    for i in range(retries):
        try:
            return translator.translate(text)
        except Exception:
            print(f"Error translating. Trying again ({i+1}/{retries})...")
            sleep(delay)
    raise Exception(f"Fail to translate after {retries} attempts.")

def translate_markdown(text, translator, delay):
    # Regex expressions
    MD_CODE_REGEX = r'```[a-z]*\n[\s\S]*?\n```'
    CODE_REPLACEMENT_KW = r'xx_markdown_code_xx'
    
    MD_LINK_REGEX = r'\[[^)]+\)'
    LINK_REPLACEMENT_KW = 'xx_markdown_link_xx'

    # Markdown tags
    END_LINE = '\n'
    IMG_PREFIX = '!['
    HEADERS = ['### ', '###', '## ', '##', '# ', '#']  # Should be from this order (bigger to smaller)

    # Inner function to replace tags from text from a source list
    def replace_from_list(tag, text, replacement_list):
        list_to_gen = lambda: [(x) for x in replacement_list]
        replacement_gen = list_to_gen()
        return re.sub(tag, lambda x: next(iter(replacement_gen)), text)

    # Inner function for translation
    def translate(text):
        # Get all markdown links
        md_links = re.findall(MD_LINK_REGEX, text)

        # Get all markdown code blocks
        md_codes = re.findall(MD_CODE_REGEX, text)

        # Replace markdown links in text to markdown_link
        text = re.sub(MD_LINK_REGEX, LINK_REPLACEMENT_KW, text)

        # Replace links in markdown to tag markdown_link
        text = re.sub(MD_CODE_REGEX, CODE_REPLACEMENT_KW, text)

        # Translate text
        text = safe_translate(translator, text, delay=delay)

        # Replace tags to original link tags
        text = replace_from_list('[Xx]' + LINK_REPLACEMENT_KW[1:], text, md_links)

        # Replace code tags
        text = replace_from_list('[Xx]' + CODE_REPLACEMENT_KW[1:], text, md_codes)

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
    lines = code.split('\n')
    translated_lines = []
    for line in lines:
        if '#' in line:
            # Split the line into code and comment parts
            code_part, comment_part = line.split('#', 1)
            # Translate the comment part using safe_translate
            translated_comment = safe_translate(translator, comment_part.strip(), delay=delay)
            # Reconstruct the line with translated comment
            translated_lines.append(f"{code_part}# {translated_comment}")
        elif 'print(f"' in line or "print(f'" in line:
            # Handle formatted print statements
            print_match = re.search(r'print\((f?)(["\'])(.*?)(\2)\)', line)
            if print_match:
                print_part = print_match.group(1)
                text_part = print_match.group(3)
                # Translate only the text within the formatted print statement
                translated_text = safe_translate(translator, text_part, delay=delay)
                # Reconstruct the line with translated text
                translated_lines.append(f'print({print_part}"{translated_text}")')
            else:
                translated_lines.append(line)  # If it doesn't match, keep the line as is
        else:
            translated_lines.append(line)
    return '\n'.join(translated_lines)

def jupyter_translate(fname, src_language, dest_language, delay, translator_name, rename_source_file=False, print_translation=False):
    """
    Translates a Jupyter Notebook from one language to another.
    """

    # Initialize the translator
    translator = get_translator(translator_name, src_language, dest_language)

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

    skip_row = False
    for i, cell in enumerate(tqdm(data_translated['cells'], desc="Translating cells", unit="cell")):
        for j, source in enumerate(cell['source']):
            if cell['cell_type'] == 'markdown':
                if source[:3] == '```':
                    skip_row = not skip_row  # Invert flag until the next code block

                if not skip_row:
                    if source not in ['```\n', '```', '\n'] and source[:4] != '<img':  # Don't translate because of:
                        # 1. ``` -> ëëë 2. '\n' disappeared 3. image links damaged
                        data_translated['cells'][i]['source'][j] = \
                            translate_markdown(source, translator, delay=delay)
            elif cell['cell_type'] == 'code':
                # Translate comments and formatted print statements within code cells
                data_translated['cells'][i]['source'][j] = \
                    translate_code_comments_and_prints(source, translator, delay=delay)

            if print_translation:
                print(data_translated['cells'][i]['source'][j])

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
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Translate a Jupyter Notebook from one language to another.")
    parser.add_argument('fname', help="Path to the Jupyter Notebook file")
    parser.add_argument('--source', default='en', help="Source language code (default: en)")
    parser.add_argument('--target', required=True, help="Destination language code")
    parser.add_argument('--delay', type=int, default=10, help="Delay between retries in seconds (default: 10)")
    parser.add_argument('--translator', default='google', help="Translator to use (options: google or mymemory). Default: google")
    parser.add_argument('--rename', action='store_true', help="Rename the original file after translation")
    parser.add_argument('--print', dest='print_translation', action='store_true', help="Print translations to console")

    args = parser.parse_args()

    jupyter_translate(
        fname=args.fname,
        src_language=args.source,
        dest_language=args.target,
        delay=args.delay,
        translator_name=args.translator,
        rename_source_file=args.rename,
        print_translation=args.print_translation
    )





