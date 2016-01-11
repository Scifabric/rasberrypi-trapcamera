#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

#try:
#    from pypandoc import convert
#    long_description = convert('README.md', 'rst')
#except IOError:
#    print("warning: README.md not found")
#    long_description = ""
#except ImportError:
#    print("warning: pypandoc module not found, could not convert Markdown to RST")
#    long_description = ""

long_description = ""

setup(
    name="pybossa-raspberry-trapcamera",
    version="0.0.1",
    author="SciFabric LTD",
    author_email="info@scifabric.com",
    description="PyBossa Raspberry Pi trap camera tool",
    long_description=long_description,
    license="AGPLv3",
    url="https://github.com/PyBossa/raspberry-trapcamera",
    classifiers = ['Development Status :: 4 - Beta',
                   'Environment :: Console',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',],
    py_modules=['pbs', 'helpers', 'exceptions'],
    install_requires=['Click', 'pybossa-client', 'flickrapi'],
    entry_points='''
        [console_scripts]
        trapcamera=trapcamera:cli
    '''
)
