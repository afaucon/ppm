import tempfile
import os

import jinja2
import jinja2.meta

import ppm.git_tool


class Template():

    def __init__(self, template_git_url):
        self.template_git_url = template_git_url

        # Create a temporary directory
        self.tempdir_object = tempfile.TemporaryDirectory()
        
        # Fork the template git into the temporary directory
        ppm.git_tool.fork(from_url=template_git_url, to_path=self.tempdir_object.name)

        # Recovering the template parameters
        self.unknown_parameters = set()

        # Process all files and directories
        for root, dirs, files in os.walk(self.tempdir_object.name, topdown=False):
            if os.path.join(self.tempdir_object.name, '.git') not in root:
                env = jinja2.Environment()

                for name in files:
                    # Find undeclared variables in the files name
                    ast = env.parse(name)
                    undeclared_variables_set = jinja2.meta.find_undeclared_variables(ast)
                    self.unknown_parameters.update(undeclared_variables_set)

                    # Find undeclared variables in the file content
                    f = open(os.path.join(root, name), "r", encoding='utf-8')
                    string = f.read()
                    f.close()
                    ast = env.parse(string)
                    undeclared_variables_set = jinja2.meta.find_undeclared_variables(ast)
                    self.unknown_parameters.update(undeclared_variables_set)
                    
                for name in dirs:
                    # Find undeclared variables in the folders name
                    ast = env.parse(name)
                    undeclared_variables_set = jinja2.meta.find_undeclared_variables(ast)
                    self.unknown_parameters.update(undeclared_variables_set)
        

    def instanciate(self, parameters):
        
        # If they are missing parameters among provided parameters, then raise an error.
        
        # Replace the generic parameters of the template by the provided parameters values.

        # Commit the result.
        pass