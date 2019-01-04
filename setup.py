# -*- coding: utf-8 -*-
import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="pfpi",
    version="1.0.0",
    author="Franklin Sarmiento",
    author_email="franklinitiel@gmail.com",
    description="Interface to do payments through Paguelo Facil gateway",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/franklintiel/pfig/wiki",
    license="MIT",
    classifiers=[
        #"Development Status :: 4 - Beta",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        'Intended Audience :: Developers',
        'Natural Language :: English',
    ],
    keywords="payments gateway paguelo-facil paguelo facil pfig",
    project_urls={
        'Documentation': "https://github.com/franklintiel/pfig",
        'Source': "https://github.com/franklintiel/pfig",
        'Tracker': "https://github.com/franklintiel/pfig/issues"
    },
    packages=setuptools.find_packages(exclude=['contrib', 'docs', 'tests*']),
    python_requires=">=2.*")
