import os
from pathlib import Path
import subprocess
import ppm
import ppm.project
import ppm.exceptions

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
        - Fork the templated repository
        raise ppm.exceptions.NotYetImplementedException
    repo = git.Repo.clone_from("git@github.com:afaucon/templated_package.git", "C:/tmp")
    print(repo.remotes.origin.refs.master)

    def required_files(self):
        """
        """
        return ppm.project.Project.required_files(self) + \
            [
                Path('src') / self.name / '__init__.py',
                Path('src') / self.name / '__main__.py',
                Path('src') / self.name / 'api.py',
                Path('src') / 'setup.py',
            ]

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
        return ppm.project.Project.required_files(self) + \
            [
                Path('src') / self.name / 'main.py',
            ]

PACKAGE = 'package'
APP = 'app'

class Checker():

    def __init__(self, project_name):
        """
        """
        self.project_name = project_name

    def __project(self, type):
        """
        """
        if type is PACKAGE:
            return Package(self.project_name)
        if type is APP:
            return App(self.project_name)

    def missing_directories(self, type):
        """
        """
        project = self.__project(type)
        return [str(dir) for dir in sorted(project.required_directories()) if not os.path.isdir(project.path / dir)] 

    def missing_files(self, type):
        """
        """
        project = self.__project(type)
        return [str(file) for file in sorted(project.required_files()) if not os.path.isfile(project.path / file)]



def get_git_remote_as_string(project_name):
    """
    """
    project = ppm.project.Project(project_name)
    git_directory = project.path / 'src'
    if os.path.isdir(git_directory):
        cp = subprocess.run(["git", "remote"], cwd=git_directory, capture_output=True)
        return cp.stdout.decode('UTF-8')
    else:
        return None

def get_git_status_as_string(project_name):
    """
    """
    project = ppm.project.Project(project_name)
    git_directory = project.path / 'src'
    if os.path.isdir(git_directory):
        cp = subprocess.run(["git", "status"], cwd=git_directory, capture_output=True)
        return cp.stdout.decode('UTF-8')
    else:
        return None



def remote_origin_is_configured(git_remote_as_string):
    """
    """
    if "origin" in git_remote_as_string:
        return True
    else:
        return False