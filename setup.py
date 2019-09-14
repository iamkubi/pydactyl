import os
import re
import sys

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
with open("pydactyl/constants.py") as fh:
    VERSION = re.search('__version__ = \'([^\']+)\'', fh.read()).group(1)

# 'setup.py publish' shortcut.
if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist bdist_wheel')
    os.system('twine upload dist/*')
    sys.exit()


setuptools.setup(
    name="py-dactyl",
    version=VERSION,
    author="Ryan Kubiak",
    author_email="iamkubi@gmail.com",
    description="An easy to use Python wrapper for the Pterodactyl Panel API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iamkubi/pydactyl",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.4',
    install_requires=[
        "requests >=2.21.0",
    ],
    tests_require=[
        "pytest >=3",
        "pytest-cov",
    ],
    project_urls={
        "Documentation": "https://pydactyl.readthedocs.io/",
        "Source": "https://github.com/iamkubi/pydactyl",
    }
)
