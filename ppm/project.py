import os.path
from pathlib import Path
import git
import ppm.exceptions


class Project:
    """
    """

    def __init__(self, name='', title='', description='', url='', author='', author_email=''):
        """
        """
        self.name = name
        self.title = title
        self.description = description
        self.url = url
        self.author = author
        self.author_email = author_email
        
        self.path = ppm.python_projects_path / name

    def create(self):
        """
        """

        def create_repository(self):
            """
            """
            # - Create the new repository on github
            # - Update the 'remote' of the local repository
            # - Push the local repository to the distant repository
            raise ppm.exceptions.NotYetImplementedException
        
        create_repository(self)

    def required_directories(self):
        """
        """
        return [
            Path('src'),
            Path('src') / '.git',
            Path('venv'),
        ]

    def required_files(self):
        """
        """
        return [
            Path('src') / self.name / '__info__.py',
            Path('src') / self.name / 'exceptions.py',
            Path('src') / '.gitignore',
            Path('src') / 'LICENSE',
            Path('src') / 'README.md',
        ]