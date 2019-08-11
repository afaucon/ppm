import git
import ppm.exceptions


class Project:
    """
    """

    def __init__(self, project_name, description, url, author, author_email):
        """
        """
        pass

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

class Package(Project):
    """
    """

    def __init__(self, project_name, package_name, description, url, author, author_email):
        """
        """
        Project.__init__(self, project_name, description, url, author, author_email)
        raise ppm.exceptions.NotYetImplementedException

    def create(self):
        """
        """
        raise ppm.exceptions.NotYetImplementedException

class App(Project):
    """
    """

    def __init__(self, project_name, app_name, description, url, author, author_email):
        """
        """
        Project.__init__(self, project_name, description, url, author, author_email)
        raise ppm.exceptions.NotYetImplementedException

    def create(self):
        """
        """
        raise ppm.exceptions.NotYetImplementedException