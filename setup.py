#-*- coding:utf-8 -*-
"""
Setup for baguette-namespace package.
"""
from setuptools import find_packages, setup

setup(
    name='baguette-namespace',
    version='0.1',
    url='baguette.io',
    download_url='baguette.io',
    author_email='dev@baguette.io',
    packages=find_packages(),
    platforms=[
        'Linux/UNIX',
        'MacOS',
        'Windows'
    ],
    install_requires=[
        'baguette-messaging',
        'kubernetes==4.0.0',
    ],
    extras_require={
        'testing': [
            'baguette-messaging[testing]',
        ],
        'doc': [
            'Sphinx',
        ],
    },
    package_data={
        'levure': ['templates/profile.tmpl'],
        'levure.tests': ['farine.ini', 'pytest.ini'],
    },
)
