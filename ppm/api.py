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
        raise ppm.exceptions.NotYetImplementedException

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

    def __init__(self, project_name, type):
        """
        """
        if type is PACKAGE:
            self.project = Package(project_name)
        else:
            self.project = App(project_name)

    def missing_directories(self):
        """
        """
        return [str(dir) for dir in sorted(self.project.required_directories()) if not os.path.isdir(self.project.path / dir)] 

    def missing_files(self):
        """
        """
        return [str(file) for file in sorted(self.project.required_files()) if not os.path.isfile(self.project.path / file)]



    def get_git_status(self):
        """
        """
        cp = subprocess.run(["git", "remote"], cwd=self.project.path / 'src', capture_output=True)
        
        if "origin" not in cp.stdout.decode('UTF-8'):
            return "remote repository not found"

        cp = subprocess.run(["git", "status"], cwd=self.project.path / 'src', capture_output=True)
        
        if (   "Changes not staged for commit" in cp.stdout.decode('UTF-8')
            or "Changes to be committed"       in cp.stdout.decode('UTF-8')):
            return "uncommitted changes"
            
        if "Your branch is ahead of 'origin/master'" in cp.stdout.decode('UTF-8'):
            return "remote outdated"
            
        if "nothing to commit, working directory clean" in cp.stdout.decode('UTF-8'):
            return "ok"
            
        return "???"