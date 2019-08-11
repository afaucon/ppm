import os.path


def get_project_type(project_path, project_name):
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

        if (    os.path.isfile(project_path / 'src' / project_name / '__info__.py')
            and os.path.isfile(project_path / 'src' / project_name / '__init__.py')
            and os.path.isfile(project_path / 'src' / project_name / '__main__.py')
            and os.path.isfile(project_path / 'src' / project_name / 'api.py')
            and os.path.isfile(project_path / 'src' / project_name / 'display.py')
            and os.path.isfile(project_path / 'src' / project_name / 'exceptions.py')
            and os.path.isfile(project_path / 'src/.gitignore')
            and os.path.isfile(project_path / 'src/LICENSE')
            and os.path.isfile(project_path / 'src/README.md')
            and os.path.isfile(project_path / 'src/setup.py')):

            return 'package'

        if (    os.path.isfile(project_path / 'src' / project_name / '__info__.py')
            and os.path.isfile(project_path / 'src' / project_name / 'main.py')
            and os.path.isfile(project_path / 'src' / project_name / 'exceptions.py')
            and os.path.isfile(project_path / 'src/.gitignore')
            and os.path.isfile(project_path / 'src/LICENSE')
            and os.path.isfile(project_path / 'src/README.md')):
            
            return 'app'

        return 'unknown'