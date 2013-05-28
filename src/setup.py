#!/usr/bin/env python

from setuptools import setup

setup(
    name='noora',
    version='0.0.8.1',
    description='noora database installer.',
    author='Jan Ripke',
    author_email='janripke@gmail.com',
    url='https://sourceforge.net/projects/noora/',
    packages=['noora'],
      long_description="""\
      NoOra is an attempt to apply a pattern to develop and install Oracle database projects, to promote portability and productivity.  ...
      """,
      classifiers=[
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Programming Language :: Python",
          "Development Status :: 5 - Production/Stable",
          "Intended Audience :: Developers",
          "Topic :: Database",
      ],
      keywords='database install tools',
      license='GPL',
      install_requires=[
        'setuptools',
        'wxpython',
      ],
      )