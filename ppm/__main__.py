import argparse
import os.path
import subprocess

# ONLY ppm can be imported because we are in the __main__.py, 
# i.e. like if we were outside of the package
import ppm



def command_list():
    """
    """    

    def git_status_summary(git_status_as_string):
        """
        """
        if git_status_as_string is None:
            return "No git status"

        if (   "Changes not staged for commit" in git_status_as_string
            or "Changes to be committed"       in git_status_as_string):
            return "uncommitted changes"
            
        if "Your branch is ahead of " in git_status_as_string:
            return "remote outdated"
            
        if "nothing to commit, working directory clean" in git_status_as_string:
            return "ok"
            
        return "???"

    projects_list = []
    for project_name in os.listdir(ppm.python_projects_path):

        checker = ppm.Checker(project_name)

        project_status = 'missing directories or files'
        if len(checker.missing_directories(ppm.PACKAGE)) and len(checker.missing_files(ppm.PACKAGE)) == 0:
            project_status = 'valid package'
        
        if len(checker.missing_directories(ppm.APP)) and len(checker.missing_files(ppm.APP)) == 0:
            project_status = 'valid app'

        projects_list.append(
            {
                'name':project_name,
                'status':project_status,
                'git':git_status_summary(ppm.get_git_status_as_string(project_name)),
            }
        )
            
    size = {'name':0,
            'status':0,
            'git':0}

    for project in projects_list:
        if size['name'] < len(project['name']):
            size['name'] = len(project['name'])
        if size['status'] < len(project['status']):
            size['status'] = len(project['status'])
        if size['git'] < len(project['git']):
            size['git'] = len(project['git'])

    print('{info:{width}}'.format(info='Project name', width=size['name']),   end='  ')
    print('{info:{width}}'.format(info='status',       width=size['status']), end='  ')
    print('{info:{width}}'.format(info='git',          width=size['git']),    end='\n')

    print('{info:-<{width}}'.format(info='', width=size['name']),   end='  ')
    print('{info:-<{width}}'.format(info='', width=size['status']), end='  ')
    print('{info:-<{width}}'.format(info='', width=size['git']),    end='\n')

    for project in projects_list:
        print('{info:{width}}'.format(info=project['name'],   width=size['name']),   end='  ')
        print('{info:{width}}'.format(info=project['status'], width=size['status']), end='  ')
        print('{info:{width}}'.format(info=project['git'],    width=size['git']),    end='\n')

def command_check_all(project_name):
    """
    """
    checker = ppm.Checker(project_name)
        
    print("Checking project structure: ", end = '')
    result, detail, step_ok = ppm.main.check_project_structure(checker)
    print(result)
    
    print("Checking project files: ", end = '')
    result, detail, step_ok = ppm.main.check_project_files(checker)
    print(result)
    
    print("Checking git status: ", end = '')
    result, detail, step_ok = ppm.main.check_git_status()
    print(result)
    
def command_open_visual_studio_code(project_name):
    """
    """
    project_path = ppm.python_projects_path / project_name
    if not os.path.isdir(project_path):
        raise ppm.exceptions.ProjectDoesNotExist
    subprocess.run(["Code", "."], cwd=project_path, shell=True)




def basic_parser():
    """

    sta: Single template action
        To get the list of the template parameters
            mimic info --get-parameters template-git-path
        To instanciate a template into a new project
            mimic instanciate template-git-path instance-path
        To check if a project is compliant with a template 
            mimic checkup [OPTIONS] template-git-path instance-path
              --only-in-template
              --only-in-instance
              --not-compliant
    
    spa: Single project action
        To start Visual Studio Code:
            spa vscode project-path
        To start Sourcetree:
            spa sourcetree project-path

    devdashm: Development dashboard configuration
        There are 2 configuration files located in $home directory.
        - .devdash/project-bkmk and to configurure bookmarked project:
            devdash-c project-bkmk -a/--add    project-path shortname
            devdash-c project-bkmk -l/--list
            devdash-c project-bkmk -d/--delete shortname
            devdash-c project-bkmk -g/--get    shortname
        - .devdash/template-bkmk and to configure bookmarked template:
            devdash-c template-bkmk -a/--add    template-git-path shortname
            devdash-c template-bkmk -l/--list
            devdash-c template-bkmk -d/--delete shortname
            devdash-c template-bkmk -g/--get    shortname

    xdevdash: Graphical development dashboard
        To view all bookmarked projects
            To add a new project to the bookmarked projects by requiring the project-path and its shortname to the user.
            To select one of the bookmarked projects
                To delete the selected project from the configuration of the bookmarked projects
                To start the selected project in Visual Studio Code
                To start the selected project in Sourcetree
                To check if the selected project is compliant to its template

        To view all bookmarked templates
            To add a new template to the bookmarked templates by requiring the template-git-path and its shortname to the user.            
            To select one of the bookmarked templates
                To delete the selected template from the configuration of the bookmarked templates
                To get the parameters list of the selected template
                To instanciate the selected template into a new project by requiring the user to enter a project-path, a shortname and if this new project must be mookmarked.

    Nouvelle architecture:
    + Project-name
        + __info__.py
        + __init__.py
        + __main__.py
        + api.py
    + venv
    + .gitignore
    + LICENSE
    + README.md
    + setup.py
    """

    basic_parser = argparse.ArgumentParser(prog=ppm.__info__.__package_name__, 
                                           description=ppm.__info__.__description__)

    subparsers = basic_parser.add_subparsers(dest="command")

    # Config command
    parser_config = subparsers.add_parser('config')

    group = parser_config.add_mutually_exclusive_group()
    group.add_argument('--global', action='store_true')
    group.add_argument('--project', '-p')

    group = parser_config.add_mutually_exclusive_group()
    group.add_argument('--list', '-l', action='store_true')
    group.add_argument('--get', nargs=1, metavar='name')
    group.add_argument('--set', nargs=2, metavar=('name', 'value'))

    # Create command
    parser_create = subparsers.add_parser('create')
    parser_create.add_argument('template', help='Path of the git repository of the templated project')

    # Checkup command
    parser_create = subparsers.add_parser('checkup')
    parser_create.add_argument('template', help='Path of the git repository of the templated project')
    parser_create.add_argument('name', help='Project name to check')

    # Develop command
    parser_vscode = subparsers.add_parser('develop')
    parser_vscode.add_argument('name', help='Project name to develop')

    # General arguments
    subparsers.add_parser('list')
    subparsers.add_parser('gui')

    # Return the basic parser
    return basic_parser

def main_procedure():
    """
    """

    parser = basic_parser()
    
    # Parse the command line
    # Note: 'parse_known_args' method does not produce an error when unknown arguments are present
    args, remaining_argv = parser.parse_known_args()

    if args.command == "config":
        pass

    if args.command == "create":

        template = ppm.Template(template_git_url=args.template)
        
        parser = argparse.ArgumentParser(parents=[parser],
                                         add_help=False)

        for unknown_parameter in template.unknown_parameters_set:
            parser.add_argument("--" + unknown_parameter, 
                                action='store',
                                required=False,
                                default='""')

        # Providing the 'template' as the 'namespace' parameter of 'parse_args'
        # allows to auto-fill the template with new attributes that are derived
        # from 'unknown_parameters_set'.
        parameters = object()
        args = parser.parse_args(remaining_argv, namespace=parameters)

        template.create_project()

    if args.command == "checkup":
        # command_status(args.name)
        pass

    if args.command == "develop":
        # command_open_visual_studio_code(args.name)
        pass

    if args.command == "list":
        # command_list()
        pass

    if args.command == "gui":
        # command_list()
        pass


main_procedure()