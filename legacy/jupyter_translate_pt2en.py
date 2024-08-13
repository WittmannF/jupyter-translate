"""
History:
- Aug 2024: Updated to include translation of comments in code cells and translation statistics, with a progress bar. (andrebelem@id.uff.br)
"""

import json, fire, os, re
from googletrans import Translator
from tqdm import tqdm  # For progress bar

def translate_markdown(text, dest_language='en'):
    # Regex expressions
    MD_CODE_REGEX = r'```[a-z]*\n[\s\S]*?\n```'
    CODE_REPLACEMENT_KW = r'xx_markdown_code_xx'
    
    MD_LINK_REGEX = r'\[[^)]+\)'
    LINK_REPLACEMENT_KW = 'xx_markdown_link_xx'

    # Markdown tags
    END_LINE='\n'
    IMG_PREFIX='!['
    HEADERS=['### ', '###', '## ', '##', '# ', '#'] # Should be from this order (bigger to smaller)

    # Inner function to replace tags from text from a source list
    def replace_from_list(tag, text, replacement_list):
        list_to_gen = lambda: [(x) for x in replacement_list]
        replacement_gen = list_to_gen()
        return re.sub(tag, lambda x: next(iter(replacement_gen)), text)

    # Create an instance of Translator
    translator = Translator()

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
        text = translator.translate(text, dest=dest_language).text

        # Replace tags to original link tags
        text = replace_from_list('[Xx]'+LINK_REPLACEMENT_KW[1:], text, md_links)

        # Replace code tags
        text = replace_from_list('[Xx]'+CODE_REPLACEMENT_KW[1:], text, md_codes)

        return text

    # Check if there are special Markdown tags
    if len(text)>=2:
        if text[-1:]==END_LINE:
            return translate(text)+'\n'

        if text[:2]==IMG_PREFIX:
            return text

        for header in HEADERS:
            len_header=len(header)
            if text[:len_header]==header:
                return header + translate(text[len_header:])

    return translate(text)

# Function to translate comments and formatted print statements in code cells
def translate_code_comments_and_prints(code, dest_language='en'):
    translator = Translator()
    lines = code.split('\n')
    translated_lines = []
    for line in lines:
        if '#' in line:
            # Split the line into code and comment parts
            code_part, comment_part = line.split('#', 1)
            # Translate the comment part
            translated_comment = translator.translate(comment_part.strip(), dest=dest_language).text
            # Reconstruct the line with translated comment
            translated_lines.append(f"{code_part}# {translated_comment}")
        elif 'print(f"' in line or "print(f'" in line:
            # Handle formatted print statements
            print_match = re.search(r'print\((f?)(["\'])(.*?)(\2)\)', line)
            if print_match:
                print_part = print_match.group(1)
                text_part = print_match.group(3)
                # Translate only the text within the formatted print statement
                translated_text = translator.translate(text_part, dest=dest_language).text
                # Reconstruct the line with translated text
                translated_lines.append(f'print({print_part}"{translated_text}")')
            else:
                translated_lines.append(line)  # If it doesn't match, keep the line as is
        else:
            translated_lines.append(line)
    return '\n'.join(translated_lines)

# Export function with statistics and progress
def jupyter_translate_pt2en(fname, rename_source_file=False, print_translation=False):
    """
    Translates a Jupyter Notebook from Portuguese to English.
    """
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
                            translate_markdown(source, dest_language='en')
            elif cell['cell_type'] == 'code':
                # Translate comments and formatted print statements within code cells
                data_translated['cells'][i]['source'][j] = \
                    translate_code_comments_and_prints(source, dest_language='en')

            if print_translation:
                print(data_translated['cells'][i]['source'][j])

    if rename_source_file:
        fname_bk = f"{'.'.join(fname.split('.')[:-1])}_bk.ipynb"  # index.ipynb -> index_bk.ipynb

        os.rename(fname, fname_bk)
        print(f'{fname} has been renamed as {fname_bk}')

        with open(fname, 'w', encoding='utf-8') as f:
            json.dump(data_translated, f, ensure_ascii=False, indent=2)
        print(f'The English translation has been saved as {fname}')
    else:
        dest_fname = f"{'.'.join(fname.split('.')[:-1])}_en.ipynb"  # any.name.ipynb -> any.name_en.ipynb
        with open(dest_fname, 'w', encoding='utf-8') as f:
            json.dump(data_translated, f, ensure_ascii=False, indent=2)
        print(f'The English translation has been saved as {dest_fname}')

def markdown_translator(input_fpath, output_fpath, input_name_suffix=''):
    with open(input_fpath, 'r', encoding='utf-8') as f:
        content = f.readlines()
    content = ''.join(content)
    content_translated = translate_markdown(content, dest_language='en')
    if input_name_suffix != '':
        new_input_name = f"{'.'.join(input_fpath.split('.')[:-1])}{input_name_suffix}.md"
        os.rename(input_fpath, new_input_name)
    with open(output_fpath, 'w', encoding='utf-8') as f:
        f.write(content_translated)

if __name__ == '__main__':
    fire.Fire(jupyter_translate_pt2en)




