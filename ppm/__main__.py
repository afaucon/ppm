import argparse
import os.path
import subprocess

# ONLY ppm can be imported because we are in the __main__.py, 
# i.e. like if we were outside of the package
import ppm


def command_create_package(package_name, project_title, description, url, author, author_email):
    """
    """
    package = ppm.Package(package_name, project_title, description, url, author, author_email)
    package.create()
    print("Package '{}' suscessfully created.".format(package_name))

def command_create_app(app_name, project_title, description, url, author, author_email):
    """
    """
    app = ppm.App(app_name, project_title, description, url, author, author_email)
    app.create()
    print("App '{}' suscessfully created.".format(app_name))

def command_list():
    """
    """
    projects_list = []
    for project_name in os.listdir(ppm.python_projects_path):

        # Check the project type
        project_type = 'unknown'
        
        checker = ppm.Checker(project_name, ppm.PACKAGE)
        if len(checker.missing_files()) == 0:
            project_type = 'package'
        
        checker = ppm.Checker(project_name, ppm.APP)
        if len(checker.missing_files()) == 0:
            project_type = 'app'

        projects_list.append({'name':project_name,
                              'type':project_type})
            
    size = {'name':0,
            'type':0}

    for project in projects_list:
        if size['name'] < len(project['name']):
            size['name'] = len(project['name'])
        if size['type'] < len(project['type']):
            size['type'] = len(project['type'])

    print('{info:{width}}'.format(info='Project name', width=size['name']), end='  ')
    print('{info:{width}}'.format(info='Type',         width=size['type']), end='\n')

    print('{info:-<{width}}'.format(info='', width=size['name']), end='  ')
    print('{info:-<{width}}'.format(info='', width=size['type']), end='\n')

    for project in projects_list:
        print('{info:{width}}'.format(info=project['name'], width=size['name']), end='  ')
        print('{info:{width}}'.format(info=project['type'], width=size['type']), end='\n')

def command_status(project_name):
    """
    """
    checker = ppm.Checker(project_name, ppm.PACKAGE)
    
def command_open_visual_studio_code(project_name):
    """
    """
    project_path = ppm.python_projects_path / project_name
    if not os.path.isdir(project_path):
        raise ppm.exceptions.ProjectDoesNotExist
    subprocess.run(["Code", "."], cwd=project_path, shell=True)

def main_procedure():
    """
    """
    parser = argparse.ArgumentParser(prog=ppm.__info__.__package_name__, 
                                     description=ppm.__info__.__description__)

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Create command
    parser_create = subparsers.add_parser('create')
    parser_create.add_argument('type', choices=['package', 'app'])
    parser_create.add_argument('name')
    parser_create.add_argument('--project_title', action='store')
    parser_create.add_argument('--description', action='store')
    parser_create.add_argument('--url', action='store')
    parser_create.add_argument('--author', action='store')
    parser_create.add_argument('--author_email', action='store')

    # List command
    subparsers.add_parser('list')

    # Status command
    parser_status = subparsers.add_parser('status')
    parser_status.add_argument('name')

    # Develop command
    parser_vscode = subparsers.add_parser('develop')
    parser_vscode.add_argument('name')

    args = parser.parse_args()

    if args.command == "create":
        if args.type == "package":
            command_create_package(args.name, args.project_title, args.description, args.url, args.author, args.author_email)
        else:
            command_create_app(args.name, args.project_title, args.description, args.url, args.author, args.author_email)
    if args.command == "list":
        command_list()
    if args.command == "status":
        command_status(args.name)
    if args.command == "develop":
        command_open_visual_studio_code(args.name)

if __name__ == "__main__":
    main_procedure()