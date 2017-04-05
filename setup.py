# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='uspto',
    version='1.0',
    description='Package to parse USPTO xml data.',
    long_description=readme,
    author='Jose Luis Rodriguez',
    author_email='jrodriguezorjuela@luc.edu',
    url='https://github.com/jlroo/uspto',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
