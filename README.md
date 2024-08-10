# Jupyter Translate: a Python script for translating Jupyter notebook files

[version 2024]

This script was created as a general-purpose translator for Jupyter notebooks, translating from English to any other language. Here’s an example of how to use it:

```
python jupyter_translate.py index.ipynb --language 'pt'
```
A new file named `index_pt.ipynb` will be created (or the code of the language you decided to use). There is also a script for automatically translating all .ipynb files in a folder and its subfolders. Additionally, you can use a version of the script that converts Portuguese notebooks to English:
```
python jupyter_translate_pt2en.py index.ipynb
```
The program translates markdown content, comments in code cells, and messages formatted in  `print(f" ... ")`. 

OBS: jupyter-translate uses [googletrans](https://py-googletrans.readthedocs.io/en/latest/) on its backend. The --language option can be set to any of the following:

| Code   | Language              | Code   | Language               | Code   | Language             | Code   | Language          |
|--------|-----------------------|--------|------------------------|--------|----------------------|--------|-------------------|
| af     | afrikaans              | sq     | albanian               | am     | amharic              | ar     | arabic            |
| hy     | armenian               | az     | azerbaijani            | eu     | basque               | be     | belarusian        |
| bn     | bengali                | bs     | bosnian                | bg     | bulgarian            | ca     | catalan           |
| ceb    | cebuano                | ny     | chichewa               | zh-cn  | chinese (simplified) | zh-tw  | chinese (traditional) |
| co     | corsican               | hr     | croatian               | cs     | czech                | da     | danish            |
| nl     | dutch                  | en     | english                | eo     | esperanto            | et     | estonian          |
| tl     | filipino               | fi     | finnish                | fr     | french               | fy     | frisian           |
| gl     | galician               | ka     | georgian               | de     | german               | el     | greek             |
| gu     | gujarati               | ht     | haitian creole         | ha     | hausa                | haw    | hawaiian          |
| iw     | hebrew                 | hi     | hindi                  | hmn    | hmong                | hu     | hungarian         |
| is     | icelandic              | ig     | igbo                   | id     | indonesian           | ga     | irish             |
| it     | italian                | ja     | japanese               | jw     | javanese             | kn     | kannada           |
| kk     | kazakh                 | km     | khmer                  | ko     | korean               | ku     | kurdish (kurmanji)|
| ky     | kyrgyz                 | lo     | lao                    | la     | latin                | lv     | latvian           |
| lt     | lithuanian             | lb     | luxembourgish          | mk     | macedonian           | mg     | malagasy          |
| ms     | malay                  | ml     | malayalam              | mt     | maltese              | mi     | maori             |
| mr     | marathi                | mn     | mongolian              | my     | myanmar (burmese)    | ne     | nepali            |
| no     | norwegian              | ps     | pashto                 | fa     | persian              | pl     | polish            |
| pt     | portuguese             | pa     | punjabi                | ro     | romanian             | ru     | russian           |
| sm     | samoan                 | gd     | scots gaelic           | sr     | serbian              | st     | sesotho           |
| sn     | shona                  | sd     | sindhi                 | si     | sinhala              | sk     | slovak            |
| sl     | slovenian              | so     | somali                 | es     | spanish              | su     | sundanese         |
| sw     | swahili                | sv     | swedish                | tg     | tajik                | ta     | tamil             |
| te     | telugu                 | th     | thai                   | tr     | turkish              | uk     | ukrainian         |
| ur     | urdu                   | uz     | uzbek                  | vi     | vietnamese           | cy     | welsh             |
| xh     | xhosa                  | yi     | yiddish                | yo     | yoruba               | zu     | zulu              |
| fil    | Filipino               | he     | Hebrew                 |        |                      |        |                   |


## Implementation notes
To set up a working Conda environment to use this tool, you must install `fire` from conda-forge and a newer version of `googletrans` via pip, as well as a few other libraries. You can do this with the included environment file. In your terminal, enter:
```
conda env create --file environment.yml
conda activate jtranslate
```
**Note**: Copy and execute each line one by one -- not as a block.

If you have any question or suggestion, use the *pull request* or discussion option in github.
