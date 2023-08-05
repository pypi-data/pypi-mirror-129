# auto-release-to-pypi
This repo is a reference code to automatically push the package to pypi on creating a github release



```
name: Upload Python Package

on:
  release:
    types: [created]

jobs:
  deploy:
    runs-on: ubuntu-20.04

    steps:
    - uses: actions/checkout@v2
    - uses: actions/setup-python@v2
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install setuptools wheel twine
    - name: Build and publish
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_PASSWORD }}
      run: |
        python setup.py sdist bdist_wheel
        twine upload dist/*

```

