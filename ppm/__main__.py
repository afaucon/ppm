import click
import ppm
import pprint


class Url(click.ParamType):
    name = "url"

    def convert(self, value, param, ctx):
        import urllib.request
        try:
            urllib.request.urlopen(value)
        except urllib.request.URLError:
            self.fail("\nBad URL: " + value, param, ctx)
        except ValueError:
            self.fail("\nBad URL: " + value, param, ctx)
        return value
        
    def __repr__(self):
        return 'URL'

class PathOrUrl(click.ParamType):
    name = "path or url"

    def __init__(self):
        self.path_param = click.Path(exists=True, file_okay=False)
        self.url_param = Url()

    def convert(self, value, param, ctx):
        error_msg_for_path = False
        error_msg_for_url = False
        try:
            self.path_param.convert(value, param, ctx)
        except click.BadParameter:
            error_msg_for_path = True

        try:
            self.url_param.convert(value, param, ctx)
        except click.BadParameter:
            error_msg_for_url = True
                
        if error_msg_for_path and error_msg_for_url:
            self.fail(value + " is not a valid path nor a valid URL.", param, ctx)
        return value

    def __repr__(self):
        return 'PATH OR URL'

@click.group()
def main():
    pass

@main.command()
@click.option('-p', '--parameters', 
              is_flag=True,
              help='Provide the list of the parameters of the template.')
@click.option('-v', '--version', 
              is_flag=True,
              help='Provide the version of the template.')
@click.argument('git-template',
                type=PathOrUrl())
def template(parameters, version, git_template):
    """
    Gets information about a generic template.
    """
    if parameters:
        template = ppm.Template(template_git_url=git_template)
        unknown_parameters_set = template.unknown_parameters_set
        print("Parameters:")
        print("===========")
        print()
        pprint.PrettyPrinter().pprint(unknown_parameters_set)
        print()

    if version:
        print("Version:")
        print("========")
        print()
        print("Not yet implemented")
        print()

@main.command()
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
                #type=PathOrUrl())
@click.argument('path', 
                type=click.Path(exists=True, file_okay=False, resolve_path=True), 
                required=False, 
                default=".")
def instanciate(configuration_file, interractive, git_template, path):
    """
    Instanciates a git template to create a new project into a local path.
    Without any option, its is similar to git clone.
    """

    # Create the template object
    template = ppm.Template(template_git_url=git_template)

    # Recovers the unknown parameters
    unknown_parameters_set = template.unknown_parameters_set

    # Open the configuration file if provided, and recover defined parameters values.
    import json
    parameters = json.load(configuration_file)
    
    # If the interractive option is activated, requires the user to enter all the missing parameters values.

    # If they are still missing parameters values, then raise an error and terminate the programm.

    # Here, a value for all the parameters has been provided.

    # Clone the git_template into a temparary directory.

    # Remove the (git) remote.

    # Replace the generic parameters by the provided parameters values.

    # Commit the result.
    pass

@main.command()
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
def checkup(only_in_template, only_in_project, different, path):
    """
    Checks if a project is compliant with a template.
    """
    pass


@main.command()
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
def ide(vscode, sourcetree, path):
    """
    Launches an ide on a project.
    """
    pass
    
if __name__ == '__main__':
    main()