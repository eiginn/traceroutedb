#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    "requests",
    "psycopg2",
    "flask",
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='traceroutedb',
    version='0.1.0',
    description="An experiment in full mesh historical traceroutes",
    long_description=readme + '\n\n' + history,
    author="Ryan Carter",
    author_email='ryan@cloudflare.com',
    url='https://github.com/eiginn/traceroutedb',
    packages=[
        'traceroutedb',
    ],
    package_dir={'traceroutedb':
                 'traceroutedb'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='traceroutedb',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
