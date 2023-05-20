#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: suralmasha - Badasyan Alexandra

import glob
from setuptools import setup, find_packages
from shutil import copytree, copy, rmtree
from os import path


def requirements():
    with open('requirements.txt', 'r', encoding='utf-8') as f_requirements:
        deps = []
        while True:
            l = f_requirements.readline()
            if l == '':
                break
            elif l.startswith('--'):
                continue
            elif l.startswith('-e'):
                url, name = l.split('#egg=')
                l = name.replace('\n', '') + ' @' + url.replace('-e', '')
            deps.append(l)
        return deps


def add_files():
    added_files = []
    for filename in glob.iglob('temp/' + '**/*.*', recursive=True):
        added_files.append(filename.replace('temp/ru_transcript/', ''))
    return added_files


def readme():
    with open('README.md', 'r', encoding='utf-8') as f_readme:
        return f_readme.read()


if __name__ == "__main__":
    sources_dir = './src'
    temp_dir = 'temp'

    # Prepare temp folders
    rmtree(temp_dir, ignore_errors=True)
    copytree(path.join(sources_dir, 'data'), path.join(temp_dir, 'ru_transcript', 'data'), copy_function=copy)
    copytree(path.join(sources_dir, 'tools'), path.join(temp_dir, 'ru_transcript', 'tools'), copy_function=copy)
    copy(path.join(sources_dir, 'RuTranscript.py'), path.join(temp_dir, 'ru_transcript', 'ru_transcript.py'))
    f = open(path.join(temp_dir, 'ru_transcript', '__init__.py'), 'w')
    f.write('from ru_transcript.ru_transcript import ru_transcript'
            '\nfrom ru_transcript.allophones_tools import get_allophone_info')
    f.close()

    setup(
        name='ru_transcript',
        version='0.1.0',
        description='Package that makes a phonetic transcription in russian.',
        long_description=readme(),
        url='https://github.com/suralmasha/RuTranscript',
        classifiers=[
            'Natural Language :: Russian',
            'Programming Language :: Python :: 3.8',
            'Topic :: Text Processing :: Linguistic :: NLP'
        ],
        author='Badasyan Alexandra',
        keywords='nlp russian transcription phonetics linguistic',
        author_email='sashabadasyan@icloud.com',

        packages=find_packages(temp_dir),
        package_dir={'': temp_dir},
        package_data={'': add_files()},
        install_requires=requirements()
    )
