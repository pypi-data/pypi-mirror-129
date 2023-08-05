#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r",encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="db2text",
    version="0.0.10",
    author="Chen chuan",
    author_email="chenc224@163.com",
    description="database to text",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/chenc224/dbt",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    scripts=["bin/dbt"],
    zip_safe= False,
    include_package_data = True,
)
