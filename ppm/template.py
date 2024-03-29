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
    """
    [summary]
    """

    def __init__(self, git_template):
        """
        [summary]
        
        :param git_template: [description]
        :type git_template: [type]
        """

        # Create a temporary directory
        self.tempdir = tempfile.TemporaryDirectory()
        self.dirpath = self.tempdir.name

        # Clone the git into the temporary directory
        git.Repo.clone_from(url=git_template, to_path=self.dirpath)

        # Create the repo object to interract with the repository cloned in the temporary directory
        repo = git.Repo(path=self.dirpath)
        
        # Because there has been a 'clone' operation, there exists a 'origin' remote ref.
        # Rename the "origin" remote into 'template'
        git.remote.Remote(repo, 'origin').rename('template')
        
        # Recovering the template parameters
        self.fsnode_parameters = set()
        self.parameters = set()

        # Process all files and directories
        for root, dirs, files in os.walk(self.dirpath):
            if os.path.join(self.dirpath, '.git') not in root:
                env = jinja2.Environment()

                # Finding undeclared variables in folders name
                for name in dirs:
                    ast = env.parse(name)
                    undeclared_variables = jinja2.meta.find_undeclared_variables(ast)
                    self.fsnode_parameters.update(undeclared_variables)
                    self.parameters.update(undeclared_variables)

                # Finding undeclared variables in files name
                for name in files:
                    ast = env.parse(name)
                    undeclared_variables = jinja2.meta.find_undeclared_variables(ast)
                    self.fsnode_parameters.update(undeclared_variables)
                    self.parameters.update(undeclared_variables)

                # Finding undeclared variables in files content
                for name in files:
                    f = open(os.path.join(root, name), "r", encoding='utf-8')
                    string = f.read()
                    f.close()
                    ast = env.parse(string)
                    undeclared_variables = jinja2.meta.find_undeclared_variables(ast)
                    self.parameters.update(undeclared_variables)
        
    def instanciate(self, parameters, destination=None):
        """
        [summary]
        
        :param parameters: [description]
        :type parameters: [type]
        :param destination: [description], defaults to None
        :type destination: [type], optional
        """

        # Create the repo object to interract with the repository cloned in the temporary directory
        repo = git.Repo(path=self.dirpath)

        # Replace the generic parameters of the template by the provided parameters values.
        for root, dirs, files in os.walk(self.dirpath):
            if os.path.join(self.dirpath, '.git') not in root:

                # Replacing undeclared variables in files content
                env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=root), undefined=jinja2.DebugUndefined)
                for filename in files:
                    file_content = env.get_template(filename).render(parameters)
                    with open(os.path.join(root, filename), "w", newline='') as fh:
                        fh.write(file_content)
                    repo.index.add(os.path.join(root, filename))

                # Replacing undeclared variables in files name
                env = jinja2.Environment(undefined=jinja2.DebugUndefined)
                for filename in files:
                    new_filename = env.from_string(filename).render(parameters)
                    if new_filename != filename:
                        repo.index.move([os.path.join(root, filename), os.path.join(root, new_filename)])

                # Replacing undeclared variables in folders name
                env = jinja2.Environment(undefined=jinja2.DebugUndefined)
                for dirname in dirs:
                    new_dirname = env.from_string(dirname).render(parameters)
                    if new_dirname != dirname:
                        repo.index.move([os.path.join(root, dirname), os.path.join(root, new_dirname)])

        # Commit the result on the branch master.
        repo.index.commit("Template instanciation")
        
        # Copy the temporary template to the destination
        if destination is not None:
            shutil.copytree(self.dirpath, destination, dirs_exist_ok=True)
