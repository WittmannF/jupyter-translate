# Jupyter Translate - Python script for translating jupyter notebook files

> NOTE: You might also want to take a loot at [nbTranslate](https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/nbextensions/nbTranslate/README.html)

This script was created with the purpose of translating the FastAI documentation (which was implemented using notebooks) into Portuguese, but can also be used for a general purpose. Here's an example of usage:

```
python jupyter_translate.py index.ipynb -language 'pt'
```

A file called `index_pt.ipynb` is going to be created. You can also specify a destination folder:

```
python jupyter_translate.py index.ipynb -language 'pt' -dest_folder '.\pt-br' 
```

