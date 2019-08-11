import argparse

import ppm.api
import ppm.display


def command_create_package(project_name, package_name, description, url, author, author_email):
    """
    """
    ppm.api.create_package(project_name, package_name, description, url, author, author_email)
    print("Package '{}' suscessfully created.".format(project_name))

def command_create_app(project_name, package_name, description, url, author, author_email):
    """
    """
    ppm.api.create_app(project_name, package_name, description, url, author, author_email)
    print("App '{}' suscessfully created.".format(project_name))

def command_list():
    """
    """
    projects_list = ppm.api.list()
    ppm.display.after_list(projects_list)

def command_open_visual_studio_code(project_name):
    """
    """
    ppm.api.open_visual_studio_code(project_name)

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
    parser_create.add_argument('--project_name', action='store')
    parser_create.add_argument('--description', action='store')
    parser_create.add_argument('--url', action='store')
    parser_create.add_argument('--author', action='store')
    parser_create.add_argument('--author_email', action='store')

    # List command
    subparsers.add_parser('list')

    # Check command
    parser_check = subparsers.add_parser('check')
    parser_check.add_argument('name')

    # Develop command
    parser_vscode = subparsers.add_parser('develop')
    parser_vscode.add_argument('name')

    args = parser.parse_args()

    if args.command == "create":
        if args.type == "package":
            command_create_package(args.project_name, args.name, args.description, args.url, args.author, args.author_email)
        else:
            command_create_app(args.project_name, args.name, args.description, args.url, args.author, args.author_email)
    if args.command == "list":
        command_list()
    if args.command == "develop":
        command_open_visual_studio_code(args.name)

if __name__ == "__main__":
    main_procedure()