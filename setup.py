#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pipenv install twine --dev

import io
import os
import sys
from shutil import rmtree

from setuptools import Command, find_packages, setup

NAME = 'pypale'
DESCRIPTION = '(Py)thon (Pa)ssword(le)ss Tokens.'
URL = 'https://github.com/anthcor/pypale'
EMAIL = 'anthcor@gmail.com'
AUTHOR = 'Anthony Corletti'
REQUIRES_PYTHON = '>=3.8.0'
# What packages are required for this module to be executed?
REQUIRED = ['PyJWT']
# What packages are optional?
EXTRAS = {}

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# README.md must be in MANIFEST.in
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = ""

# Load the package's __version__.py module as a dictionary.
about = {}
project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
with open(os.path.join(here, project_slug, '__version__.py')) as f:
    exec(f.read(), about)


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(
            sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(about['__version__']))
        os.system('git push --tags')

        sys.exit()


setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(
        exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: PyPy',
        'License :: OSI Approved :: MIT License'
    ],
    # setup.py publish support
    cmdclass={
        'upload': UploadCommand,
    },
)
