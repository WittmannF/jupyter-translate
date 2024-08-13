# Using `jupyter-translate` in google colab

Imagine you have a few notebooks in your google drive and you want to use `jupyter-translate` to translate it ! YES, it's possible ! Just follow these instructions:

- open a new google colab
- mount your google drive
- use `!pip install jupyter-translate` to install it
- navigate in your drive (on the left side of colab) to the location where you have a notebook `.ipynb`
- right click on it and "copy path" (for example '/content/drive/MyDrive/Colab Notebooks/whatever_en.ipynb')
- just run jupyter_translate in the code cell like `!jupyter_translate '/content/drive/MyDrive/Colab Notebooks/whatever_en.ipynb' --source en --target pt`
- Voilà... You now have a version named  `whatever_en_pt.ipynb` in the same location.

  
