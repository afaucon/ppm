import click
import logging
import os.path
import pprint

import ppm
import ppm.config_templates


def parse_cli_template_parameters(cli_template_parameters, template_parameters):
    """
    This function parses the template parameters provided by the command line
    and returns a dictionary of all the template parameters with their value.
    
    Arguments:
        cli_template_parameters -- the template parameters recovered from the command line.
        template_parameters -- the parameters defined by the template itself.
    
    Returns:
        [dict] -- The template parameters with their value
    """
    parser = click.OptionParser()
    for param in template_parameters:
        parser.add_option(["--" + param], param)
    return parser.parse_args(list(cli_template_parameters))[0]

def get_user_defined_parameters(configuration_file, interractive, template_parameters_from_cli, template_parameters):
    """
    TODO: Description to write
    """
    # Define the variable for storing the parameters defined by the user
    user_parameters = {}
    
    # If a configuration file is provided,
    # then recover defined parameters values from it.
    if configuration_file:
        import json
        new_parameters_definition = json.load(configuration_file)
        for param_name in new_parameters_definition:
            if param_name in template.parameters:
                 user_parameters[param_name] = new_parameters_definition[param_name]
            else:
                logging.info("Parameter provided in configuration is useless: {}".format(param_name))
    
    # if template parameters have been defined within the command line
    # then a 2nd parsing of the cli must be done to recover the parameters values.
    if len(template_parameters_from_cli) != 0:
        new_parameters_definition = parse_cli_template_parameters(template_parameters_from_cli, template_parameters)
        for param_name in new_parameters_definition:
            if user_parameters.get(param_name) is None:
                user_parameters[param_name] = new_parameters_definition[param_name]
            else:
                raise click.BadParameter("Template parameter has been defined twice: {}".format(param_name))

    # If the interractive option is activated,
    # then require the user to enter the missing parameters values.
    if interractive:
        for param_name in template.parameters:
            if user_parameters.get(param_name) is None:
                user_parameters[param_name] = click.prompt(param_name)
    
    return user_parameters

@click.group()
@click.option('-v', '--verbose', type=click.IntRange(min=0, max=2), default=0)
def ppm_cli(verbose):
    if verbose == 0:
        logging.basicConfig(level=logging.WARNING)
    if verbose == 1:
        logging.basicConfig(level=logging.INFO)
    if verbose == 2:
        # TODO: In this mode, DEBUG log from imported packages are displayed.
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
        string = pprint.PrettyPrinter().pformat(template.parameters)
        print(string) # TODO: Do not use print within a Click application.

@ppm_cli.command(context_settings=dict(
    ignore_unknown_options=True,
))
@click.option('-c', '--configuration-file', 
              type=click.File(), 
              help='Configures template parameters with a configration file. This file must be json formatted.')
@click.option('-i', '--interractive', 
              is_flag=True,
              help='Prompts the user to enter a value for the generic parameters, whose values have not been specified with the parameter file. Each parameter whose value has not been returned by the user will take the value from the template.')
@click.argument('git-template')
@click.argument('destination', 
                type=click.Path(exists=True, file_okay=False, dir_okay=True, writable=True), 
                required=False, 
                default=".")
@click.argument('template_parameters', nargs=-1, type=click.UNPROCESSED)
def instanciate(configuration_file, interractive, git_template, destination, template_parameters):
    """
    Instanciates a git template to create a new project into a local path.
    Without any option, its is similar to git clone.
    """

    # Create the template object
    template = ppm.Template(git_template=git_template)

    # Get parameters defined by the user
    user_parameters = get_user_defined_parameters(
        configuration_file=configuration_file, 
        interractive=interractive,
        template_parameters_from_cli=template_parameters,
        template_parameters=template.parameters)

    # If they are missing parameters among provided parameters, then log an information for the user.
    for param_name in template.parameters:
        if user_parameters.get(param_name) is None:
            logging.warning("Template instanciation with undefined parameter: {}".format(param_name))

    # Instanciate the template
    template.instanciate(user_parameters, destination)

@ppm_cli.command(context_settings=dict(
    ignore_unknown_options=True,
))
@click.option('-c', '--configuration-file', 
              type=click.File(), 
              help='Configures template parameters with a configration file. This file must be json formatted.')
@click.option('-i', '--interractive', 
              is_flag=True,
              help='Prompts the user to enter a value for the generic parameters, whose values have not been specified with the parameter file. Each parameter whose value has not been returned by the user will take the value from the template.')
@click.argument('git-template')
@click.argument('directory',
                type=click.Path(exists=True, file_okay=False, resolve_path=True), 
                required=False, 
                default=".")
@click.argument('template_parameters', nargs=-1, type=click.UNPROCESSED)
def checkup(configuration_file, interractive, directory, git_template, template_parameters):
    """
    Checks if a directory is compliant with a template.
    """

    # Create the template object
    template = ppm.Template(git_template=git_template)

    # Get parameters defined by the user
    user_parameters = get_user_defined_parameters(
        configuration_file=configuration_file, 
        interractive=interractive,
        template_parameters_from_cli=template_parameters,
        template_parameters=template.fsnode_parameters)
    
    # Instanciate the template
    template.instanciate(user_parameters)

    # Analyze if the provided directory is compliant with the template
    _, uncompliances = ppm.is_compliant(instance=directory, template=template.dirpath)

    for uncompliance in uncompliances:
        print(uncompliance['relpath'] + ': ' + uncompliance['reason']) # TODO: Use click log instead of print

    # TODO: Find a common ancestor with git.


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

@ppm_config_templates_cli.command(name='list')
def list_command():
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