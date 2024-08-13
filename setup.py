from setuptools import setup, find_packages

setup(
    name="jupyter-translate",
    version="2024.0",
    author="Fernando Marcos Wittmann & Andre Belem",
    description="A Python script for translating Jupyter notebook files.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/WittmannF/jupyter-translate",  # Replace with your GitHub repo
    packages=find_packages(),
    include_package_data=True,
    install_requires=open('requirements.txt').read().splitlines(),
    entry_points={
        'console_scripts': [
            'jupyter_translate=jupyter_translate:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Or your license
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',  # Specify the minimum Python version required
)
