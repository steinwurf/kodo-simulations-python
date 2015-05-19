#! /usr/bin/env python
# encoding: utf-8

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Kodo Python Simulations',
    'author': 'Steinwurf ApS',
    'url': '',
    'download_url': '',
    'author_email': 'jpihl@steinwurf.com',
    'version': '0.1',
    'install_requires': ['nose', 'kodo'],
    'packages': ['simulator'],
    'scripts': [],
    'name': 'kodo-simulations-python'
}

setup(**config)
