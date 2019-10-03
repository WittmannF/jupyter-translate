# Jupyter Translate - Python script for translating Jupyter notebook files

> NOTE: You might also want to take a loot at [nbTranslate](https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/nbextensions/nbTranslate/README.html)

This script was created with the purpose of translating the FastAI documentation (which was implemented using notebooks) into Portuguese, but can also be used for a general purpose. Here's an example of usage:

```
python jupyter_translate.py index.ipynb -language 'pt'
```

The original file is going to be renamed to `index_bk.ipynb` and the file named `index.ipynb` is going have the translated version. It was done this way in order to avoid having to rename all translated files later. 

There's also a script for automatically translate all .ipynb files from a folder and it's subfolders. Keep in mind that all .ipynb files are going to be renamed to `{file_name}_bk.ipynb`
