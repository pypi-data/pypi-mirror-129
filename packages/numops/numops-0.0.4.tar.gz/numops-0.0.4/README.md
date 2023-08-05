# auto-release-to-pypi
This repo is a reference code to automatically push the package to pypi on creating a github release


Add a file in `.github\workflows\publish-to-pypi.yml` and copy paste below content.

```yaml
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
        TWINE_USERNAME: ${{ secrets.PYPI_USERNAME }}
        TWINE_PASSWORD: ${{ secrets.PYPI_PASSWORD }}
      run: |
        python setup.py sdist bdist_wheel
        twine upload dist/*
```

**Step 2:** Update PYPI Creds
Next add pypi credentials in github secrets.
- PYPI_USERNAME
- PYPI_PASSWORD

**Step 3:** Create a release tag
On creationg of release tag, github action will automatically start building wheel file and push them to pypi