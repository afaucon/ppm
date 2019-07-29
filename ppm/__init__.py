def get_python_projects_path():
    import os.path
    import ppm.exceptions

    python_projects_path = os.environ.get('PYTHON_PRJ')

    if python_projects_path is None:
        raise ppm.exceptions.UndefinedPythonProjectsPath()
    if not os.path.isdir(python_projects_path):
        raise ppm.exceptions.PythonProjectsPathDoesNotExist()

    return python_projects_path
    
import pathlib

python_projects_path = pathlib.Path(get_python_projects_path())


from .__info__ import __description__
from .__info__ import __url__
from .__info__ import __version__
from .__info__ import __author__
from .__info__ import __author_email__
from .__info__ import __license__
from .__info__ import __copyright__


from .api import create_package, create_app, list, develop
