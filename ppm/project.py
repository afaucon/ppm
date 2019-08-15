import os.path
from pathlib import Path
import git
import ppm.exceptions


class Project:
    """
    """

    def __init__(self, name, title, description, url, author, author_email):
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
            # 1/ Clone the templated repository
            # 2/ Create the new repository on github
            # 3/ Update the 'remote' of the local repository
            # 4/ Push the local repository to the distant repository
            raise ppm.exceptions.NotYetImplementedException
            repo = git.Repo.clone_from("git@github.com:afaucon/templated_package.git", "C:/tmp")
            print(repo.remotes.origin.refs.master)
        
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