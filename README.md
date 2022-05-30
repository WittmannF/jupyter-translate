# Jupyter Translate - Python script for translating Jupyter notebook files

> NOTE: You might also want to take a look at [nbTranslate](https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/nbextensions/nbTranslate/README.html)
(no longer maintained)

This script was created with the purpose of translating the FastAI documentation (which was implemented using notebooks) into Portuguese, but can also be used for a general purpose. Here's an example of usage:

```
python jupyter_translate.py index.ipynb --language 'pt'
```

A new file with the name `index_pt.ipynb` is going to be created. There's also a script for automatically translate all .ipynb files from a folder and it's subfolders.

OBS: jupyter-translate uses [googletrans](https://py-googletrans.readthedocs.io/en/latest/) on its backend. `-language` can be any from the following dictionary:
```
{'af': 'afrikaans',
 'sq': 'albanian',
 'am': 'amharic',
 'ar': 'arabic',
 'hy': 'armenian',
 'az': 'azerbaijani',
 'eu': 'basque',
 'be': 'belarusian',
 'bn': 'bengali',
 'bs': 'bosnian',
 'bg': 'bulgarian',
 'ca': 'catalan',
 'ceb': 'cebuano',
 'ny': 'chichewa',
 'zh-cn': 'chinese (simplified)',
 'zh-tw': 'chinese (traditional)',
 'co': 'corsican',
 'hr': 'croatian',
 'cs': 'czech',
 'da': 'danish',
 'nl': 'dutch',
 'en': 'english',
 'eo': 'esperanto',
 'et': 'estonian',
 'tl': 'filipino',
 'fi': 'finnish',
 'fr': 'french',
 'fy': 'frisian',
 'gl': 'galician',
 'ka': 'georgian',
 'de': 'german',
 'el': 'greek',
 'gu': 'gujarati',
 'ht': 'haitian creole',
 'ha': 'hausa',
 'haw': 'hawaiian',
 'iw': 'hebrew',
 'hi': 'hindi',
 'hmn': 'hmong',
 'hu': 'hungarian',
 'is': 'icelandic',
 'ig': 'igbo',
 'id': 'indonesian',
 'ga': 'irish',
 'it': 'italian',
 'ja': 'japanese',
 'jw': 'javanese',
 'kn': 'kannada',
 'kk': 'kazakh',
 'km': 'khmer',
 'ko': 'korean',
 'ku': 'kurdish (kurmanji)',
 'ky': 'kyrgyz',
 'lo': 'lao',
 'la': 'latin',
 'lv': 'latvian',
 'lt': 'lithuanian',
 'lb': 'luxembourgish',
 'mk': 'macedonian',
 'mg': 'malagasy',
 'ms': 'malay',
 'ml': 'malayalam',
 'mt': 'maltese',
 'mi': 'maori',
 'mr': 'marathi',
 'mn': 'mongolian',
 'my': 'myanmar (burmese)',
 'ne': 'nepali',
 'no': 'norwegian',
 'ps': 'pashto',
 'fa': 'persian',
 'pl': 'polish',
 'pt': 'portuguese',
 'pa': 'punjabi',
 'ro': 'romanian',
 'ru': 'russian',
 'sm': 'samoan',
 'gd': 'scots gaelic',
 'sr': 'serbian',
 'st': 'sesotho',
 'sn': 'shona',
 'sd': 'sindhi',
 'si': 'sinhala',
 'sk': 'slovak',
 'sl': 'slovenian',
 'so': 'somali',
 'es': 'spanish',
 'su': 'sundanese',
 'sw': 'swahili',
 'sv': 'swedish',
 'tg': 'tajik',
 'ta': 'tamil',
 'te': 'telugu',
 'th': 'thai',
 'tr': 'turkish',
 'uk': 'ukrainian',
 'ur': 'urdu',
 'uz': 'uzbek',
 'vi': 'vietnamese',
 'cy': 'welsh',
 'xh': 'xhosa',
 'yi': 'yiddish',
 'yo': 'yoruba',
 'zu': 'zulu',
 'fil': 'Filipino',
 'he': 'Hebrew'}
 ```

## Implementation notes
To set up a working conda environment to use this tool, you must install `fire` with conda-forge
and a newer version of `googletrans` with pip. Like this:
```
conda env create --file environment.yml
conda activate jtranslate
pip install googletrans==3.1.0a0
```
Copy and execute each line one by one -- not as a block.
