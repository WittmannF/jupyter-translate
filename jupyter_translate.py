import json, fire, os, re
from googletrans import Translator


def translate_markdown(text, dest_language='pt'):
    # Regex expressions
    MD_CODE_REGEX='```[a-z]*\n[\s\S]*?\n```'
    CODE_REPLACEMENT_KW = 'xx_markdown_code_xx'

    MD_LINK_REGEX="\[[^)]+\)"
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

    # Create an instance of Tranlator
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

#export
def jupyter_translate(fname, language='pt', rename_source_file=False, print_translation=False):
    """
    TODO:
    add dest_path: Destination folder in order to save the translated files.
    """
    data_translated = json.load(open(fname, 'r'))

    skip_row=False
    for i, cell in enumerate(data_translated['cells']):
        for j, source in enumerate(cell['source']):
            if cell['cell_type']=='markdown':
                if source[:3]=='```':
                    skip_row = not skip_row # Invert flag until I find next code block

                if not skip_row:
                    data_translated['cells'][i]['source'][j] = \
                        translate_markdown(source, dest_language=language)
            if print_translation:
                print(data_translated['cells'][i]['source'][j])

    if rename_source_file:
        fname_bk = f"{'.'.join(fname.split('.')[:-1])}_bk.ipynb" # index.ipynb -> index_bk.ipynb

        os.rename(fname, fname_bk)
        print(f'{fname} has been renamed as {fname_bk}')

        open(fname,'w').write(json.dumps(data_translated))
        print(f'The {language} translation has been saved as {fname}')
    else:
        dest_fname = f"{'.'.join(fname.split('.')[:-1])}_{language}.ipynb" # any.name.ipynb -> any.name_pt.ipynb
        open(dest_fname,'w').write(json.dumps(data_translated))
        print(f'The {language} translation has been saved as {dest_fname}')

def markdown_translator(input_fpath, output_fpath, input_name_suffix=''):
    with open(input_fpath,'r') as f:
        content = f.readlines()
    content = ''.join(content)
    content_translated = translate_markdown(content)
    if input_name_suffix!='':
        new_input_name=f"{'.'.join(input_fpath.split('.')[:-1])}{input_name_suffix}.md"
        os.rename(input_fpath, new_input_name)
    with open(output_fpath, 'w') as f:
        f.write(content_translated)


if __name__ == '__main__':
    fire.Fire(jupyter_translate)
