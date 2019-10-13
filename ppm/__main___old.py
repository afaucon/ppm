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
        dpm
    ===
    
    Usage: dpm [OPTIONS] COMMAND [ARGS]...
    
    Options:
      --help  Show this message and exit.
    
    Commands:
      checkup      Check if a project is compliant with a template.
      ide          Launche an ide on a project.
      instanciate  Instanciate a git template to create a new project into a...
      template     Get information about a generic template.
    
    dpm template
    ============
    
    Usage: dpm template [OPTIONS] GIT_TEMPLATE
    
      Get information about a generic template.
    
    Options:
      -p, --parameters  Provide the list of the parameters of the template.
      -v, --version     Provide the version of the template.
      --help            Show this message and exit.
    
    dpm instanciate
    ===============
    
    Usage: dpm instanciate [OPTIONS] GIT_TEMPLATE [PATH]
    
      Instanciate a git template to create a new project into a local path.
      Without any option, its is similar to git clone.
    
    Options:
      -c, --configuration-file FILE  Configure template parameters with a
                                     configration file. This file must be json
                                     formatted.
      -i, --interractive             Prompt the user to enter a value for each
                                     generic parameters, whose values have not
                                     been specified with the parameter file. Each
                                     parameter whose value has not been returned
                                     by the user will take the value from the
                                     template.
      --help                         Show this message and exit.
    
    dpm checkup
    ===========
    
    Usage: dpm checkup [OPTIONS] [PATH]
    
      Check if a project is compliant with a template.
    
    Options:
      -t, --only-in-template  Return files that are in the template an not in the
                              project.
      -p, --only-in-project   Return files that are in the project an not in the
                              template.
      -d, --different         Return files that are different between the project
                              and the template.
      --help                  Show this message and exit.
    
    dpm ide
    =======
    
    Usage: dpm ide [OPTIONS] [PATH]
    
      Launche an ide on a project.
    
    Options:
      --vscode      Launche visual studio code.
      --sourcetree  Launche sourcetree.
      --help        Show this message and exit.


      

    Operation on all projects
    -------------------------

        There is a configuration file located in $home directory: .devdash/projects
        To configurure bookmarked projects:
            ppm projects -a/--add    shortname [project-path]
            ppm projects -l/--list
            ppm projects -d/--delete shortname
            ppm projects -g/--get    shortname

    Operation on all templates
    --------------------------

        There is a configuration file located in $home directory: .devdash/templates
        To configure bookmarked templates:
            ppm templates -a/--add    template-git-path shortname
            ppm templates -l/--list
            ppm templates -d/--delete shortname
            ppm templates -g/--get    shortname



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

    # Template command
    parser_template = subparsers.add_parser('merge')
    groupA = parser_template.add_argument_group('When merge is on-going')
    excl_group = groupA.add_mutually_exclusive_group(required=True)
    excl_group.add_argument('--continue', action='store_true')
    excl_group.add_argument('--abort', action='store_true')
    excl_group.add_argument('--quit', action='store_true')
    groupB = parser_template.add_argument_group('Start a merge')
    groupB.add_argument('--no-commit', action='store_true')
    groupB.add_argument('-m', metavar='<msg>')
    groupB.add_argument('commit', metavar='<commit>')
    
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