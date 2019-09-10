import tempfile
import os

import jinja2
import jinja2.meta

import ppm.git_tool


class Template():

    def __init__(self, template_git_path):
        self.template_git_path = template_git_path

        # Create a temporary directory
        self.tempdir_object = tempfile.TemporaryDirectory()
        
        # Fork the template git into the temporary directory
        ppm.git_tool.fork_repository(template_git_path, self.tempdir_object.name)

        # Recovering the template parameters
        self.unknown_parameters_set = set()

        # ... from the names of files and directories
        for root, dirs, files in os.walk(self.tempdir_object.name, topdown=False):
            if os.path.join(self.tempdir_object.name, '.git') not in root:
                env = jinja2.Environment()

                for name in files:
                    # Find undeclared variables in the file name
                    ast = env.parse(name)
                    undeclared_variables_set = jinja2.meta.find_undeclared_variables(ast)
                    self.unknown_parameters_set.update(undeclared_variables_set)

                    # Find undeclared variables in the file content
                    f = open(os.path.join(root, name), "r", encoding='utf-8')
                    string = f.read()
                    f.close()
                    ast = env.parse(string)
                    undeclared_variables_set = jinja2.meta.find_undeclared_variables(ast)
                    self.unknown_parameters_set.update(undeclared_variables_set)
                    
                for name in dirs:
                    ast = env.parse(name)
                    undeclared_variables_set = jinja2.meta.find_undeclared_variables(ast)
                    self.unknown_parameters_set.update(undeclared_variables_set)

        # ... and from the files content
        

    def create_project(self):
        pass