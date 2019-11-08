import click
import logging
import os.path
import pprint

import ppm
import ppm.config_templates


CONFIG_FILE = ".ppm"


@click.group()
@click.option('-v', '--verbose', type=click.IntRange(min=0, max=2), default=0)
def ppm_cli(verbose):
    if verbose == 0:
        logging.basicConfig(level=logging.WARNING)
    if verbose == 1:
        logging.basicConfig(level=logging.INFO)
    if verbose == 2:
        # Todo: In this mode, DEBUG log from imported packages are displayed.
        # Example: DEBUG:git.cmd:Popen(['git', 'clone', ...
        logging.basicConfig(level=logging.DEBUG)

@ppm_cli.command()
@click.option('-p', '--parameters', 
              is_flag=True,
              help='Provide the list of the parameters of the template.')
@click.argument('git-template')
def template(parameters, git_template):
    """
    Gets information about a generic template.
    """
    if parameters:
        template = ppm.Template(git_template=git_template)
        unknown_parameters_set = template.unknown_parameters
        string = pprint.PrettyPrinter().pformat(unknown_parameters_set)
        print(string) # Todo: Do not use print within a Click application.

@ppm_cli.command()
@click.option('-c', '--configuration-file', 
              type=click.File(), 
              help='Configures template parameters with a configration file. This file must be json formatted.')
@click.option('-i', '--interractive', 
              is_flag=True,
              help='Prompts the user to enter a value for each generic parameters, whose values have not been specified with the parameter file. Each parameter whose value has not been returned by the user will take the value from the template.')
@click.argument('git-template')
@click.argument('destination', 
                type=click.Path(exists=True, file_okay=False, dir_okay=True, writable=True), 
                required=False, 
                default=".")
def instanciate(configuration_file, interractive, git_template, destination):
    """
    Instanciates a git template to create a new project into a local path.
    Without any option, its is similar to git clone.
    """

    # Create the template object
    template = ppm.Template(git_template=git_template)

    # Recovers the unknown parameters from the template. 
    user_parameters = {}
    
    # If the configuration file is provided,
    # then recover defined parameters values from it.
    if configuration_file:
        import json
        file_parameters = json.load(configuration_file)
        for param_name in file_parameters:
            if param_name in template.unknown_parameters:
                 user_parameters[param_name] = file_parameters[param_name]
            else:
                logging.info("Parameter provided in configuration is useless: {}".format(param_name))
    
    # If the interractive option is activated,
    # then require the user to enter the missing parameters values.
    if interractive:
        for param_name in template.unknown_parameters:
            if user_parameters.get(param_name) is None:
                user_parameters[param_name] = click.prompt(param_name)
    
    # If they are missing parameters among provided parameters, then log an information for the user.
    for param_name in template.unknown_parameters:
        if user_parameters.get(param_name) is None:
            logging.warning("Template instanciation with undefined parameter: {}".format(param_name))

    # Instanciate the template
    template.instanciate(user_parameters, destination)

@ppm_cli.command()
@click.argument('git-template')
@click.argument('directory',
                type=click.Path(exists=True, file_okay=False, resolve_path=True), 
                required=False, 
                default=".")
def checkup(directory, git_template):
    """
    Checks if a directory is compliant with a template.
    """

    # Create the template object
    template = ppm.Template(git_template=git_template)

    # Analyze if the provided directory is compliant with the template
    _, uncompliances = ppm.is_compliant(instance=directory, template=template.dirpath)

    for uncompliance in uncompliances:
        print(uncompliance['relpath'] + ': ' + uncompliance['reason'])



@click.group()
@click.option('-v', '--verbose', type=click.IntRange(min=0, max=2), default=0)
def ppm_config_templates_cli(verbose):
    if verbose == 0:
        logging.basicConfig(level=logging.WARNING)
    if verbose == 1:
        logging.basicConfig(level=logging.INFO)
    if verbose == 2:
        logging.basicConfig(level=logging.DEBUG)

@ppm_config_templates_cli.command()
@click.argument('git-template')
def add(git_template):
    """
    Adds a git template into the bookmarked templates.
    """
    ppm.config_templates.add_template(git_template)

@ppm_config_templates_cli.command()
@click.argument('git-template')
def remove(git_template):
    """
    Removes a git template from the bookmarked templates.
    """
    ppm.config_templates.remove_template(git_template)

@ppm_config_templates_cli.command()
def list():
    """
    Lists the bookmarked templates.
    """
    for template in ppm.config_templates.get_templates():
        click.echo('- ' + template)




@click.command()
@click.option('--vscode', 
              is_flag=True,
              help='Launches visual studio code.')
@click.option('--sourcetree', 
              is_flag=True,
              help='Launches sourcetree.')
@click.argument('path', 
                type=click.Path(exists=True, file_okay=False, resolve_path=True), 
                required=False, 
                default=".")
def ppm_ide_cli(vscode, sourcetree, path):
    """
    Launches an ide on a project.
    """
    pass
    


    
if __name__ == '__main__':
    import sys
    eval(sys.argv[1])(sys.argv[2:])