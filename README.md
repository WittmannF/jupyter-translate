# Jupyter Translate: a Python script for translating Jupyter notebook files

[version 2024]

This script was created as a general-purpose translator for Jupyter notebooks, translating across different languages (the default source language is English). Install it with:
```
pip install jupyter_translate
```

After installed, you can use it but running the following command in the terminal:

```
jupyter_translate tests/data/test_Notebook_en.ipynb --target pt
```
A new file named `test_Notebook_en_pt.ipynb` will be created (or the code of the language you decided to use). 

### Translate Multiple Notebooks in a Directory

You can translate all notebooks in a directory by using the `--directory` flag or by simply providing a directory path:

```
jupyter_translate tests/data --target es --directory
```

By default, this will recursively traverse all subdirectories. If you want to translate only the notebooks in the specified directory (without subdirectories), add the `--no-recursive` flag:

```
jupyter_translate tests/data --target es --directory --no-recursive
```

You can also translate notebooks from/to any language:
```
jupyter_translate tests/data/test_Notebook_pt.ipynb --source pt --target en
```

The program translates markdown content, comments in code cells, and messages formatted in  `print(f" ... ")`. 

## Translator Options:

By default, jupyter-translate uses [googletrans](https://py-googletrans.readthedocs.io/en/latest/) on its backend. However, you can specify a different translator using the --translator option. Here's how to use it:

```
jupyter_translate test_Notebook_en.ipynb --target pt --translator='mymemory'
```
Currently supported translators are:
* google (default)
* mymemory
 <br> 
**Caution:** If you are using `mymemory` as backend translator, the language codes are different. The script will show you the codes. Make sure to specify the correct `--source` and `--target` language codes supported by the selected translator. The --language option can be set to any of the following (codes from default `googletrans`:

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

### Other options:

`--delay`:<br>
The delay in seconds between retries in case of connection issues. The default is 10 seconds. Adjusting this can help if you're facing connectivity issues, especially behind firewalls.
```
jupyter_translate my_notebook.ipynb --target es --delay=15
```

`--rename`:<br>
If specified, this option will rename the original notebook file after the translation is complete. This can be useful if you want to keep the translated version as the primary file.
```
jupyter_translate my_notebook.ipynb --target es --rename
```

`--print`:<br>
Use this option if you want to print the translations directly to the console as they happen.
```
jupyter_translate my_notebook.ipynb --target es --print
```

`--directory`:<br>
Process all .ipynb files in the specified directory. This can be used with a directory path to translate all notebooks in that location.
```
jupyter_translate notebooks_dir/ --target es --directory
```

`--no-recursive`:<br>
When used with `--directory`, this flag prevents subdirectories from being processed. Only notebooks in the specified directory will be translated.
```
jupyter_translate notebooks_dir/ --target es --directory --no-recursive
```

## Implementation notes:

To set up a working Conda environment to use this tool, you must install a newer version of `deep-translator` via pip, as well as a few other libraries. You can do this with the included environment file. In your terminal, enter:
```
conda env create --file environment.yml
conda activate jtranslate
```

You can also reset the environment by running:
```
conda deactivate
conda remove --name jtranslate --all
conda env create -f environment.yml
conda activate jtranslate
```


**Note:** Copy and execute each line one by one—do not run them as a block. **Caution:** The googletrans API, as used by deep-translator, may face connectivity issues if you're behind a firewall. To improve accessibility in such environments, consider using the --delay option to introduce a pause between retries.

If you have any question or suggestion, use the *pull request* or discussion option in github.
