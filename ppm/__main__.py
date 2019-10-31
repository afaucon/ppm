import click
import logging
import os.path
import pprint

import ppm
import ppm.config_templates


CONFIG_FILE = ".ppm"


@click.group()
def ppm_cli():
    pass

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
        print(string) # Do not use print

@ppm_cli.command()
@click.option('-c', '--configuration-file', 
              type=click.File(), 
              help='Configures template parameters with a configration file. This file must be json formatted.')
@click.option('-i', '--interractive', 
              is_flag=True,
              help='Prompts the user to enter a value for each generic parameters, whose values have not been specified with the parameter file. Each parameter whose value has not been returned by the user will take the value from the template.')
@click.option('-f', '--force', 
              is_flag=True,
              help='Forces the instance creation even if there are undefined parameters.')
@click.argument('git-template')
@click.argument('destination', 
                type=click.Path(exists=True, file_okay=False, dir_okay=True, writable=True), 
                required=False, 
                default=".")
def instanciate(configuration_file, interractive, force, git_template, destination):
    """
    Instanciates a git template to create a new project into a local path.
    Without any option, its is similar to git clone.
    """

    # Create the template object
    template = ppm.Template(git_template=git_template)

    # Recovers the unknown parameters from the template.
    unknown_parameters = template.unknown_parameters
    parameters = {parameter:None for parameter in unknown_parameters}

    # If the configuration file is provided,
    # then recover defined parameters values from it.
    if configuration_file:
        import json
        file_parameters = json.load(configuration_file)
        for elem in file_parameters:
            if elem in parameters:
                 parameters[elem] = file_parameters[elem]
            else:
                # Todo: Inform the user with a warning with logging.
                pass
    
    # If the interractive option is activated,
    # then require the user to enter the missing parameters values.
    if interractive:
        for elem in parameters:
            if parameters[elem] is None:
                parameters[elem] = click.prompt(elem)

    # If the force option is activated,
    # then fill missing parameters values with empty string. 
    if force:
        for elem in parameters:
            if parameters[elem] is None:
                parameters[elem] = ""
    
    # Instanciate the template
    template.instanciate(parameters, destination)

@ppm_cli.command()
@click.option('-t', '--only-in-template', 
              is_flag=True,
              help='Returns files that are in the template an not in the project.')
@click.option('-p', '--only-in-project', 
              is_flag=True,
              help='Returns files that are in the project an not in the template.')
@click.option('-d', '--different', 
              is_flag=True,
              help='Returns files that are different between the project and the template.')
@click.argument('path', 
                type=click.Path(exists=True, file_okay=False, resolve_path=True), 
                required=False, 
                default=".")
@click.argument('git-template')
def checkup(only_in_template, only_in_project, different, path, git_template):
    """
    Checks if a project is compliant with a template.
    """
    pass






class TemplateOptions(click.Choice):
    name = "template options"

    mutually_exclusion_options_def = {
        'add': {
            'options': ['a', 'add'],
            'help': '',
        },
        'remove': {
            'options': ['r', 'remove'],
            'help': '',
        },
        'get_parameters': {
            'options': ['p', 'parameters', 'list_parameters'],
            'help': 'Provide the list of the parameters of the template.',
        },
        'list_templates': {
            'options': ['l', 'list'],
            'help': '',
        },
        'show_templates': {
            'options': ['s', 'show'],
            'help': '',
        },
    }

    def __init__(self):
        choices = []
        for key in TemplateOptions.mutually_exclusion_options_def:
            choices = choices + TemplateOptions.mutually_exclusion_options_def[key]['options']
        click.Choice.__init__(self, choices)

    def convert(self, value, param, ctx):
        return click.Choice.convert(self, value, param, ctx)

    def __repr__(self):
        return 'TEMPLATE OPTIONS'


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