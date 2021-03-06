import setuptools

setuptools.setup(
    name='odoo_utilities',  
    version='0.2',
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
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
)