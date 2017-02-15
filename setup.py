"""Packaging settings."""

from os.path import abspath, dirname

import pypandoc
from setuptools import setup

from formica import __version__

this_dir = abspath(dirname(__file__))
long_description = pypandoc.convert_file('README.md', 'rst')

setup(
    name='formica-cli',
    version=__version__,
    description='Simple AWS CloudFormation stack management tooling.',
    long_description=long_description,
    url='https://github.com/flomotlik/formica',
    author='Florian Motlik',
    author_email='flo@flomotlik.me',
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: Public Domain',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='cloudformation, aws, cloud',
    packages=['formica'],
    install_requires=['troposphere==1.9.2', 'boto3==1.4.4', 'click==6.7', 'texttable==0.8.7', 'awacs==0.6.1'],
    entry_points={
        'console_scripts': [
            'formica=formica.cli:main',
        ],
    },
    test_suite="tests"
)
