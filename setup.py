#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 11:34:45 2020

@author: silasjimmy
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ImageDataGen-silasjimmy",
    version="0.0.1",
    author="Silas Jimmy",
    author_email="jimmysilas17@gmail.com",
    description="A small module to get image data stored locally.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/silasjimmy/image-data-generator.git",
    packages=setuptools.find_packages(),
    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)