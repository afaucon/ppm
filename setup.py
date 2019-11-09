import os
from setuptools import setup, find_packages


package_name = "ppm"


python_requires = ">=3.8"

# Justificationss
#   If GitPython clones a repository in a temporary directory
#   then, at the end of the program when the temporary directory is about to be deleted,
#   a permission denied error occurs, for python 3.7 and below.
#   The standard python library 'tempdir' should not raise this error. 
#   https://github.com/python/cpython/pull/10320
#   The issue has been corrected in version 3.8


dependency_links = [
]

# Justifications
#   None


install_requires = [
    "click",
    "gitpython",
    "jinja2"
]

# Justifications
#   Click is used for the CLI
#   gitpython it used to clone a template, and to commit modification
#   jinja2 template engine is used for the instanciation


entry_points = {
    'console_scripts': [
        'ppm-template = ppm.__main__:ppm_template_cli',
        'ppm-project = ppm.__main__:ppm_project_cli',
        'ppm-config-templates = ppm.__main__:ppm_config_templates_cli',
    ],
    'gui_scripts': [
    ]
}


# ------------------------------------------------------------------------------

about = {}
with open(os.path.join(package_name, '__info__.py'), 'r') as f:
    exec(f.read(), about)

with open('README.md', 'r') as f:
    readme = f.read()

setup(
    name=package_name,
    version=about['__version__'],
    description=about['__description__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    license=about['__license__'],
    packages=find_packages(),
    long_description=readme,
    long_description_content_type='text/markdown',
    python_requires=python_requires,
    dependency_links=dependency_links,
    install_requires=install_requires,
    entry_points=entry_points,
)
