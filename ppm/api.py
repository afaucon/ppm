import os
import subprocess
import ppm
import ppm.project
import ppm.exceptions
import ppm.tool


class Package(ppm.project.Project):
    """
    """

    def __init__(self, package_name, project_title='', description='', url='', author='', author_email=''):
        """
        """
        ppm.project.Project.__init__(self, package_name, project_title, description, url, author, author_email)

    def create(self):
        """
        """
        raise ppm.exceptions.NotYetImplementedException

    def required_files(self):
        """
        """
        return ('src' / self.name / '__init__.py',
                'src' / self.name / '__main__.py',
                'src' / self.name / 'api.py',
                'src/setup.py')

    def missing_files(self):
        """
        """
        the_missing_files = ppm.project.Project.missing_files(self)
        for file in self.required_files():
            if not os.path.isfile(file):
                the_missing_files.append(file)
        return the_missing_files

class App(ppm.project.Project):
    """
    """

    def __init__(self, app_name, project_title='', description='', url='', author='', author_email=''):
        """
        """
        ppm.project.Project.__init__(self, app_name, project_title, description, url, author, author_email)

    def create(self):
        """
        """
        raise ppm.exceptions.NotYetImplementedException

    def required_files(self):
        """
        """
        return ('src' / self.name / 'main.py',)

    def missing_files(self):
        """
        """
        the_missing_files = ppm.project.Project.missing_files(self)
        for file in self.required_files():
            if not os.path.isfile(file):
                the_missing_files.append(file)
        return the_missing_files

def get_project(project_name):
    """
    """
    project_path = ppm.python_projects_path / project_name
    if ppm.tool.get_project_type(project_path, project_name) is 'package':
        return Package(project_name)
    elif ppm.tool.get_project_type(project_path, project_name) is 'app':
        return App(project_name)
    else:
        return None