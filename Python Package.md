# Python package

## Installer les packets nécessaires

```bash
sudo python -m pip install --upgrade pip setuptools wheel
sudo python -m pip install tqdm
sudo python -m pip install --user --upgrade twine
```


## Créer le fichier setup.py

This file must NOT be in the package.
you should have a folder tree like
```
folder
├── Package
│   ├── __init__.py
|   ├── ...
└── setup.py

```

```
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='odoo_utilities',  
    version='0.1',
    author="Gallay David",
    author_email="davidtennis96@hotmail.com",
    description="Set of tools for Odoo ERP",
    setup_requires=['setuptools-markdown'],
    long_description_content_type="text/markdown",
    long_description_markdown_filename='README.md',
    url="https://github.com/divad1196/odoo_utilities",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v",
        "Operating System :: OS Independent",
    ],
)
```

| **Meta-Data**                 | **Description**                                              |
| ----------------------------- | ------------------------------------------------------------ |
| name                          | Name of your package.                                        |
| version                       | Current version of your pip package.                         |
| scripts                       | List of executable files. It's recommended to keep them the same as your pip package name. Here we are using `dokr`. |
| author and author_email       | Name and Email Id of the author.                             |
| description                   | A short description of the package.                          |
| long_description              | A description of the package.                                |
| long_description_content_type | A longer description. Here it is markdown. We are picking README.md for the long description. |
| packages                      | Use for other package dependencies.                          |
| classifiers                   | Contains all the classifiers of your project.                |

## Compile the package

```bash
python3 setup.py sdist bdist_wheel
```

This will create 3 folders

* build: package informations
* dist: contain .whl builds (Wheel format), those are installable using `pip install some_package.whl`
* project.egg.info: egg package (bytecode, dependency links, ...)

## Upload on pip

upload with 

```bash
python3 -m twine upload dist/*
```



Optional: create file `.pypirc` in your home to remember credentials for pypi

```ini
[distutils] 
index-servers=pypi

[pypi] 
repository = https://upload.pypi.org/legacy/ 
username=divad1196
password=...
```