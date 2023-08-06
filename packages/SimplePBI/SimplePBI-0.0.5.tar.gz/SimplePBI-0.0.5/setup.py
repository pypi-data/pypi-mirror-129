'''
  /¯¯¯¯¯¯¯¯¯\
 /           \
|   |   __    |  *********************************************
|   |  |  \   |  Code writen by Ignacio and Martin.
|   |  |  |   |
|   |__|_ |   |  Sponsored by La Data Web 
|	   |__/   |  *********************************************
 \            /
  \__________/
  
'''

from setuptools import find_packages, setup

classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
]

setup(
    name='SimplePBI',
    packages=find_packages(),
    version='0.0.5',
    project_urls={
        'Documentation': 'https://docs.microsoft.com/en-us/rest/api/power-bi/',
        'Say Thanks!': 'https://www.ladataweb.com.ar/contacto.html',
        'Source': 'https://github.com/ladataweb/SimplePBI',
        'Tracker': 'https://github.com/ladataweb/SimplePBI/issues'
    },
    download_url='',
    url='',
    description='Simplify usage of Power Bi Rest API',
    long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
    long_description_content_type="text/markdown",
    author='Ignacio Barrau <igna_barrau@hotmail.com>, Martin Zurita <martinzurita1@gmail.com>',
    license='MIT',
    classifiers=classifiers,
    install_requires=[
        'requests', 
        'pandas'
    ],
    keywords=['Power BI', 'Azure', 'Data', 'Python']
)
