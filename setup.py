#!/bin/bash
# -*- coding: utf-8 -*-
import codecs
import os
import re
import setuptools

setuptools.setup(
    name='Email App',
    version='1.0',
    author='John PENDENQUE',
    author_email='pendenquejohn@gmail.com',
    license='MII',

    description='Email application to construct mass email patterns for mass emailing',
    long_description='Many times you might have wanted to construct emails using a file of names.',
    keywords='emailing email emails',

    url='https://github.com/Zadigo/EmailsApp',
    project_urls={
        # "Bug Tracker": "https://bugs.example.com/HelloWorld/",
        "Documentation": "https://github.com/Zadigo/EmailsApp/blob/master/README.md",
        # "Source Code": "https://code.example.com/HelloWorld/",
    },

    install_requires=['beautifulsoup>=0.3'],

    packages=setuptools.find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    
    classifiers=[
        'Development Status :: 1 - Beta',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ]
)
