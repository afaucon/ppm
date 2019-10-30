import tempfile
import os

import git

import jinja2
import jinja2.meta

import shutil


class TemplateException(Exception):
    """
    The generic class for all exceptions raised by Template objects.
    It is not meant to be directly instantiated.
    """
    
class instanciationException(TemplateException):
    """
    This exception is raised by the method `instanciate` in case:
    - there are not enough parameters provided to specialised completly the generic template.
    """
    
class Template():

    def __init__(self, git_template):

        # Create a temporary directory
        self.tempdir = tempfile.TemporaryDirectory()
        self.tempdirpath = self.tempdir.name

        # Clone the git into the temporary directory
        git.Repo.clone_from(url=git_template, to_path=self.tempdirpath)
        self.repo = git.Repo(path=self.tempdirpath) # Be careful: 'path' must contain an existing .git folder.

        # Todo: Prettier alternative. Check if it works!
        # repo = git.Repo.clone_from(url=git_template, to_path=self.tempdirpath)
        
        # Because there has been a 'clone' operation, there exists a 'origin' remote ref.
        # Rename the "origin" remote into 'template'
        git.remote.Remote(self.repo, 'origin').rename('template')

        # Recovering the template parameters
        self.unknown_parameters = set()
        # Process all files and directories
        for root, dirs, files in os.walk(self.tempdirpath, topdown=False):
            if os.path.join(self.tempdirpath, '.git') not in root:
                env = jinja2.Environment()

                # Finding undeclared variables in folders name
                for name in dirs:
                    ast = env.parse(name)
                    undeclared_variables_set = jinja2.meta.find_undeclared_variables(ast)
                    self.unknown_parameters.update(undeclared_variables_set)

                # Finding undeclared variables in files name
                for name in files:
                    ast = env.parse(name)
                    undeclared_variables_set = jinja2.meta.find_undeclared_variables(ast)
                    self.unknown_parameters.update(undeclared_variables_set)

                # Finding undeclared variables in files content
                for name in files:
                    f = open(os.path.join(root, name), "r", encoding='utf-8')
                    string = f.read()
                    f.close()
                    ast = env.parse(string)
                    undeclared_variables_set = jinja2.meta.find_undeclared_variables(ast)
                    self.unknown_parameters.update(undeclared_variables_set)
        
    def instanciate(self, parameters, destination):

        # If they are missing parameters among provided parameters, then raise an error.
        for unknown_parameter in self.unknown_parameters:
            if unknown_parameter not in parameters:
                raise instanciationException

        # Replace the generic parameters of the template by the provided parameters values.
        for root, dirs, files in os.walk(self.tempdirpath, topdown=False):
            if os.path.join(self.tempdirpath, '.git') not in root:
                env = jinja2.Environment()

                # Replacing undeclared variables in folders name
                for dirname in dirs:
                    # Call git mv if folder has been renamed
                    new_dirname = jinja2.Template(dirname).render(parameters)
                    print(new_dirname)
                    if new_dirname != dirname:
                        self.repo.index.move([dirname, new_dirname])
                        pass

                # Replacing undeclared variables in files name
                for filename in files:
                    # Call git mv if file has been renamed
                    pass

                # Replacing undeclared variables in files content
                for filename in files:
                    # Call git add if file has been modified
                    pass

        # Commit the result on the branch master.
        self.repo.index.commit("Template instanciation")
        del self.repo
        
        # Finally, copy the temporary template to the final destination
        shutil.copytree(self.tempdirpath, destination)