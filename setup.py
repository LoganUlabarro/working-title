"""setup."""
from setuptools import setup

setup(
    name='working-title',
    version='0.0.1',
    description='A python-based wavefront sensing module',
    long_description='',
    license='Copyright (C) 2017-2018 Logan Ulabarro & Brandon Dube, all rights reserved',
    author='Brandon Dube',
    author_email='brandondube@gmail.com',
    packages=['wt'],
    install_requires=[
        'ruamel.yaml',
        'pandas',
        'python-dotenv',
        'flask',
        'flask-wtf'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ]
)
