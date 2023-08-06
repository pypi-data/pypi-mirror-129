# Github Actions to update package on pypi 
  This repo is a reference code to automatically push the latest package release to pypi on creating a github release tags.

<br>

  #### Table of Content
  - [Add required files for pypi](#step-1-add-required-files)
  - [Update PYPI Credentials](#step-2-update-pypi-credentials)
  - [Create package release](#step-3-create-package-release)

<br>

---

### Step 1: Add required files

  Pypi requires following files to build a package
  - setup.py
  - setup.cfg
  - README.md

  Create a new file `.github\workflows\publish-to-pypi.yml` and copy paste below content.

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
---

### Step 2: Update PYPI Credentials

  Next add pypi credentials in github secrets with following Keys under settings -> secrets.
  - PYPI_USERNAME
  - PYPI_PASSWORD

  ![github action secret](https://github.com/vivekkya/auto-release-to-pypi/blob/main/docs/images/actions_secrets.JPG?raw=True)

---

### Step 3: Create package release

After files are inplace and pypi credentials has been updated in github repo secrets, next step is to create a release tag in the repo, which will trigger github actions to run workflow defined in `.github\workflows\publish-to-pypi.yml`, leading to deployment of package in pypi.

Below GIF covers all the key steps involved

![demo gif](https://github.com/vivekkya/auto-release-to-pypi/blob/main/docs/videos/demo.gif?raw=True)


1. **Create a release tag** :
On creation of release tag, github action will automatically start building distribution files and push them to pypi

2. **Check Actions** : Check whether workflow actions has initiated or not.

3. **Validate package updation in pypi** :  To validate whether package has been pushed to pypi or not. Visit pypi website and search for the package name 

4. **Install updated package** : Run below pip command to install package.
  
  ```
  pip install packagename==version
  ```