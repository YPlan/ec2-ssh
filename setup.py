#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import codecs
import os
import re

from setuptools import setup


def get_version(filename):
    with codecs.open(filename, 'r', 'utf-8') as fp:
        contents = fp.read()
    return re.search(r"__version__ = ['\"]([^'\"]+)['\"]", contents).group(1)


version = get_version(os.path.join('ec2_ssh.py'))

with codecs.open('README.rst', 'r', 'utf-8') as readme_file:
    readme = readme_file.read()

with codecs.open('HISTORY.rst', 'r', 'utf-8') as history_file:
    history = history_file.read().replace('.. :changelog:', '')


console_scripts = [
    'ec2-ssh = ec2_ssh:main',
    'ec2-host = ec2_ssh:host',
]


setup(
    name="ec2-ssh",
    version=version,
    author="Adam Johnson",
    author_email="me@adamj.eu",
    description="SSH into EC2 instances via tag name",
    long_description=readme + '\n\n' + history,
    license="MIT",
    url="https://github.com/adamchainz/ec2-ssh",
    keywords=["amazon", "aws", "ec2", "ami", "ssh", "cloud", "boto"],
    install_requires=['boto3>=1.1.0'],
    py_modules=['ec2_ssh'],
    entry_points={'console_scripts': console_scripts},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.5',
        "Topic :: Utilities"
    ],
)
