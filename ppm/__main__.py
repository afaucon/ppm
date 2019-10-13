import click


class Url(click.ParamType):
    name = "url"

    def convert(self, value, param, ctx):
        import urllib.request
        try:
            urllib.request.urlopen(value)
        except urllib.request.URLError:
            self.fail("\nBad URL: " + value, param, ctx)

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
def template(parameters, version):
    """
    Gets information about a generic template.
    """
    pass


@main.command()
@click.option('-c', '--configuration-file', 
              type=click.Path(exists=True, dir_okay=False), 
              help='Configures template parameters with a configration file. This file must be json formatted.')
@click.option('-i', '--interractive', 
              is_flag=True,
              help='Prompts the user to enter a value for each generic parameters, whose values have not been specified with the parameter file. Each parameter whose value has not been returned by the user will take the value from the template.')
@click.argument('git-template',
                type=PathOrUrl())
@click.argument('path', 
                type=click.Path(exists=True, file_okay=False, resolve_path=True), 
                required=False, 
                default=".")
def instanciate(configuration_file, interractive, git_template, path):
    """
    Instanciates a git template to create a new project into a local path.
    Without any option, its is similar to git clone.
    """
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