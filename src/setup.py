#!/usr/bin/env python

from setuptools import setup

setup(
    name='noora',
    version='1.0.2',
    description='noora database project development.',
    author='Jan Ripke',
    author_email='janripke@gmail.com',
    url='https://sourceforge.net/projects/noora/',
    packages=['noora'],
      long_description="""\
      NoOra is an attempt to apply a pattern to develop and install Oracle database projects, to promote portability and productivity.  ...
      """,
      classifiers=[
          "License :: OSI Approved :: Apache License 2.0",
          "Programming Language :: Python",
          "Development Status :: 5 - Production/Stable",
          "Intended Audience :: Developers",
          "Topic :: Database",
      ],
      keywords='database install tools',
      license='Apache License 2.0',
      install_requires=[
        'setuptools',
        'wxpython',
      ],
      )
