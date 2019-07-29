import os.path
import ppm


class Checker():

    def __init__(self, project_name):
        """
        """
        self.project_name = project_name
        self.project_path = ppm.python_projects_path / project_name
        self.result = {'type':'',
                       'git status':''}

    def get_project_type(self):
        """
        ## Project structure for a package

        - src
          - package_name
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

        - src
          - app_name
            - `__info__.py`
            - `main.py`
            - `exceptions.py`
          - `.gitignore`
          - `LICENSE`
          - `README.md`
        """

        if (    os.path.isfile(self.project_path / 'src' / self.project_name / '__info__.py')
            and os.path.isfile(self.project_path / 'src' / self.project_name / '__init__.py')
            and os.path.isfile(self.project_path / 'src' / self.project_name / '__main__.py')
            and os.path.isfile(self.project_path / 'src' / self.project_name / 'api.py')
            and os.path.isfile(self.project_path / 'src' / self.project_name / 'display.py')
            and os.path.isfile(self.project_path / 'src' / self.project_name / 'exceptions.py')
            and os.path.isfile(self.project_path / 'src/.gitignore')
            and os.path.isfile(self.project_path / 'src/LICENSE')
            and os.path.isfile(self.project_path / 'src/README.md')
            and os.path.isfile(self.project_path / 'src/setup.py')):

            return 'package'

        if (    os.path.isfile(self.project_path / 'src' / self.project_name / '__info__.py')
            and os.path.isfile(self.project_path / 'src' / self.project_name / 'main.py')
            and os.path.isfile(self.project_path / 'src' / self.project_name / 'exceptions.py')
            and os.path.isfile(self.project_path / 'src/.gitignore')
            and os.path.isfile(self.project_path / 'src/LICENSE')
            and os.path.isfile(self.project_path / 'src/README.md')):
            
            return 'app'

        return 'unknown'

    def get_venv_status(self):
        """
        """
        if not os.path.isdir(self.project_path / 'venv'):
            return 'Not found'
        else:
            return 'Found'

    def get_git_status(self):
        """
        """
        if not os.path.isdir(self.project_path / 'src/.git'):
            return 'local repository not found'
        else:
            return 'local repository found'
