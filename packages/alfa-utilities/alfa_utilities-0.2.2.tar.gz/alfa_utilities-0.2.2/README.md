# Agglomerative Late Fusion Algorithm (ALFA) Utilities

## Overview
This python package contains all ALFA related utilities, so that the base detectors and the ALFA detector can interact with each other.

## Usage

### Manual installation
* Navigate to the root folder (with the 'setup.py'):
    ```bash
    cd path/to/root/folder/
    ```
* Build:
    ```bash
    python setup.py sdist
    ```
* Install:
    ```bash
    python setup.py install
    ```

### Automatic installation
* Navigate to the root folder (with the 'setup.py'):
    ```bash
    cd path/to/root/folder/
    ```
* To use the 'upload-to-PyPI'-functionality of 'setup.py', you must:
    ```bash
    pip install twine
    ```
* Build:
    ```bash
    python setup.py sdist
    ```
* Upload to PyPI (via twine), PYyPI account is required, enter PyPI account credentials, * is placeholder for the specific .tar.gz-file:
    ```bash
    twine upload dist/*
    ```
* Install (via pip):
    ```bash
    pip install alfa_utilities
    ```

### Version
* Update:
    ```bash
    pip install alfa_utilities --upgrade (or -U)
    ```
* List:
    ```bash
    pip list (or freeze)
    ```