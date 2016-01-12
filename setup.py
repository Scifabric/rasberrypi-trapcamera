#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

long_description = "A command line tool for Raspberry Pi that captures pictures \
    using the PiCamera, uploads them to Flickr and creates a PyBossa task to \
    analyze the captured picture with the crowd."

setup(
    name="pybossa-raspberry-trapcamera",
    version="0.0.2",
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
    py_modules=['trapcamera', 'helpers'],
    install_requires=['Click', 'pybossa-client', 'flickrapi'],
    entry_points='''
        [console_scripts]
        trapcamera=trapcamera:cli
    '''
)
