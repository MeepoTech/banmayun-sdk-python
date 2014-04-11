#!/usr/bin/env python

import os
import sys

from setuptools import setup

parent_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

INSTALL_REQUIRES = ['urllib3']

setup(name='banmayun',
      version='1.0.0-prealpha',
      description='Official Banmayun REST API Client',
      author='Banmayun, Inc.',
      author_email='admin@banmayun.com',
      url='http://www.banmayun.com/',
      packages=['banmayun'],
      install_requires=INSTALL_REQUIRES,
      license=license)
