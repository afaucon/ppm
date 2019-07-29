# ppm - Python project manager

This package allows to manage python projects.

## Installation

### For users

Install the package [from GitHub](https://pip.pypa.io/en/stable/reference/pip_install/#git).

```bash
(venv) C:\Users\Adrien>pip install git+https://github.com/afaucon/ppm.git@v0.0.1
(venv) C:\Users\Adrien>pip list
```

### For developpers

Clone the package from GitHub and install it in editable mode (i.e. [setuptools "develop mode"](https://setuptools.readthedocs.io/en/latest/setuptools.html#development-mode)).

```bash
(venv) C:\Users\Adrien>git clone git+https://github.com/afaucon/ppm.git
(venv) C:\Users\Adrien>pip install --editable ppm
(venv) C:\Users\Adrien>pip list
```

### Set the python projects location in a environment variable

Set the environment variable to the directory in which all the python projects are located.

```bash
(venv) C:\Users\Adrien>set PYTON_PRJ "path/to/my/python/projects"
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

ppm.create_package("package_name")
ppm.create_app("application_name")
ppm.list()
ppm.develop("vscode", "package_name or application_name")
```

With the command line interface:

```bash
(venv) C:\Users\Adrien>python -m ppm create package package_name
(venv) C:\Users\Adrien>python -m ppm create app application_name
(venv) C:\Users\Adrien>python -m ppm list
(venv) C:\Users\Adrien>python -m ppm develop vscode [package_name|application_namme]
```

Or directly:

```bash
(venv) C:\Users\Adrien>ppm create package package_name
(venv) C:\Users\Adrien>ppm create app application_name
(venv) C:\Users\Adrien>ppm list
(venv) C:\Users\Adrien>ppm devlop vscode [package_name|application_namme]
```

## Project structure for a package

- venv
- src
  - .git
  - templated_package
    - `__info__.py`
    - `__init__.py`
    - `__main__.py`
    - `api.py`
    - `display.py`
    - `exceptions.py`
  - `.gitignore`
  - `LICENSE`
  - `README.md`
  - `setup.py`

## Project structure for an app

- venv
- src
  - .git
  - templated_app
    - `__info__.py`
    - `main.py`
    - `exceptions.py`
  - `.gitignore`
  - `LICENSE`
  - `README.md`

## Create usage

## List usage

This command lists all projects and analyze if it is a package or an app.
It also give the git status.

1. Project type: { unknown | package | app }
2. Git status  : { local repository not found | remote repository not found | uncommitted changes | ok }

```bash
(venv) C:\Users\Adrien>ppm list
Project                           Type    Git status
--------------------------------- ------- ----------
AllMyRunkeeperOnGoogleMaps        Package ok
ClientServerSocketExample         Unknown ok
DjangoChannels                    Package uncommitted changes
fauconblommaert_website           App     uncommitted changes
flasky                            App     ok
GestionActions                    Package ok
GetLabels_python                  App     remote repository not found
git_test                          Package remote repository not found
Google Apps Script                Package ok
ImageMetadata                     App     ok
ImageRenamer                      App     ok
ImmowebTracker                    App     ok
jokegetter                        App     ok
ListeCadeaux                      Unknown local repository not found
Plan_electrique_maison            Package ok
ppm                               Package ok
templated_application             App     ok
templated_package                 Package remote repository not found
ThreadingProcessSubprocessExample App     ok
Viessmann-boiler-monitoring       App     uncommitted changes
```
