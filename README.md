# ppm - Python project manager

This package allows to manage python projects.

## Installation

### For users

Install the package [from GitHub](https://pip.pypa.io/en/stable/reference/pip_install/#git).

```bash
>> pip install git+https://github.com/afaucon/ppm.git@v0.0.1
>> pip list
```

### For developpers

Clone the package from GitHub and install it in editable mode (i.e. [setuptools "develop mode"](https://setuptools.readthedocs.io/en/latest/setuptools.html#development-mode)).

```bash
>> git clone git+https://github.com/afaucon/ppm.git
>> pip install --editable ppm
>> pip list
```

### Set the python projects location in a environment variable

Set the environment variable to the directory in which all the python projects are located.

```bash
>> set PYTON_PRJ "path/to/my/python/projects"
```

Note:

- `set` modifies the current shell's (the window's) environment values, and the change is available
immediately, but it is temporary. The change will not affect other shells that are running, and as soon as
you close the shell, the new value is lost until such time as you run set again.
- `setx` modifies the value permanently, which affects all future shells, but does not modify the
environment of the shells already running. You have to exit the shell and reopen it before the change will
be available, but the value will remain modified until you change it again.

## Usage

Within a python module:

```python
import ppm

print(ppm.__author__)
print(ppm.__version__)

ppm.create.create_package("package_name")
ppm.create.create_application("application_name")
ppm.list()
ppm.report("package_name or application_name")
ppm.reports()
ppm.develop("vscode", "package_name or application_name")
```

With the command line interface:

```bash
>> python -m ppm create package package_name
>> python -m ppm create app application_name
>> python -m ppm list
>> python -m ppm report [package_name|application_namme]
>> python -m ppm reports
>> python -m ppm develop vscode [package_name|application_namme]
```

Or directly:

```bash
>> ppm create package package_name
>> ppm create app application_name
>> ppm list
>> ppm report [package_name|application_namme]
>> ppm reports
>> ppm devlop vscode [package_name|application_namme]
```

## Report

The report starts by identifying if the project is a package or an application by checking the project structure.

Example of a report content in case of a package:

1. Project type: package
2. Structure conformity: Pass
3. Common files content
   1. `.gitignore`: Pass
   2. `LICENSE`: Pass
   3. `README.md`: Pass
   4. `setup.py`: Pass
   5. package_name
      3. `__info__.py`: Pass
      1. `__init__.py`: Pass
      2. `__main__.py`: Pass
4. Git repository
   1. Local repository presence: Pass
   2. Remote repository presence: Pass
   3. Git status: Pass

## Project structure for a package

- venv
- src
  - .git
  - templated_package
    - `__info__.py`
    - `__init__.py`
    - `__main__.py`
  - `.gitignore`
  - `LICENSE`
  - `README.md`
  - `setup.py`

## Project structure for an app

- venv
- src
  - .git
  - templated_package
    - `__info__.py`
    - `main.py`
  - `.gitignore`
  - `LICENSE`
  - `README.md`
