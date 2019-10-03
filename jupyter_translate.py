import json, fire, os
from googletrans import Translator

def translate_markdown(text, dest_language='pt'):
    # Markdown tags
    END_LINE='\n'
    IMG_PREFIX='!['
    HEADERS=['### ', '###', '## ', '##', '# ', '#'] # Should be from this order (bigger to smaller)

    # Create an instance of Tranlator
    translator = Translator()

    # Inner function for translation
    def translate(text):
        return translator.translate(text, dest=dest_language).text

    # Check if there are special Markdown tags
    # TODO: Implent `code tag` and [link tag]() checker
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

def jupyter_translate(fname, language='pt', rename_source_file=True, print_translation=False):
    data_translated = json.load(open(fname, 'r'))

    for i in range(len(data_translated['cells'])):
        for j in range(len(data_translated['cells'][i]['source'])):
            if data_translated['cells'][i]['cell_type']=='markdown':
                data_translated['cells'][i]['source'][j] = \
                  translate_markdown(data_translated['cells'][i]['source'][j], dest_language=language)
            if print_translation:
                print(data_translated['cells'][i]['source'][j])

    if rename_source_file:
        fname_bk = f"{'.'.join(fname.split('.')[:-1])}_bk.ipynb" # index.ipynb -> index_bk.ipynb
        
        os.rename(fname, fname_bk)
        print(f'{fname} was renamed into {fname_bk}')
        
        open(fname,'w').write(json.dumps(data_translated))
        print(f'The {language} translation was stored in {fname}')
    else:
        dest_fname = f"{'.'.join(fname.split('.')[:-1])}_{language}.ipynb" # any.name.ipynb -> any.name_pt.ipynb
        open(dest_fname,'w').write(json.dumps(data_translated))
        print(f'The {language} translation was stored in {dest_fname}')

if __name__ == '__main__':
    fire.Fire(jupyter_translate)
