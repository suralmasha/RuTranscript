#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: suralmasha - Badasyan Alexandra

import os
from setuptools import setup, find_packages
from shutil import copytree, copy, rmtree, ignore_patterns
from os.path import join


if __name__ == "__main__":
    # Package constants
    PACKAGE_NAME = 'ru_transcript'
    PACKAGE_VERSION = '1.0'
    PACKAGE_DESCRIPTION = 'Phonetic transcription in russian'
    PACKAGE_SOURCES_URL = 'https://github.com/suralmasha/RuTranscript'

    # Variables
    sources_dir = './src'
    temp_dir = 'temp'
    excluded_files = ignore_patterns('setup.py', '.git', 'dist', 'tests', 'example.py', 'jpt_example.ipynb')

    # Prepare temp folders
    rmtree(temp_dir, ignore_errors=True)
    copytree(sources_dir, join(temp_dir, 'ru_transcript'), copy_function=copy, ignore=excluded_files)

    # Read long_description
    with open('README.md', encoding='utf8') as f:
        long_description = f.read().splitlines()

    # Read requirements from file excluded comments
    with open('requirements.txt', encoding='utf8') as f:
        install_requires = f.read().splitlines()

    # Prepare data files
    data_files = [join('data', '*.txt'), join('data', '.xlsx')]

    # Classifiers
    classifiers = [
        'Natural Language :: Russian',
        'Programming Language :: Python :: 3.8',
        'Topic :: Text Processing :: Linguistic :: NLP'
    ]

    # Build package
    setup(
        name=PACKAGE_NAME,  # package name
        version=PACKAGE_VERSION,  # version
        description=PACKAGE_DESCRIPTION,  # short description
        long_description=long_description,
        url=PACKAGE_SOURCES_URL,  # package URL
        author='Badasyan Alexandra',
        author_email='sashabadasyan@icloud.com',
        classifiers=classifiers,
        keywords='nlp russian transcription phonetics linguistic',
        install_requires=install_requires,  # list of packages this package depends on
        packages=find_packages(temp_dir), # return a list of str representing the packages it could find in source dir
        package_dir={'': temp_dir},  # set up sources dir
        package_data={'': data_files},  # append all external files to package
        include_package_data=True,
        zip_safe=False
    )
