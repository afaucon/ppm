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
    
    def check_project_structure():
        """
        """
        missing_directories_for_package = checker.missing_directories(ppm.PACKAGE)
        missing_directories_for_app = checker.missing_directories(ppm.APP)
        
        if len(missing_directories_for_package) == 0 or len(missing_directories_for_app) == 0:
            result = 'Pass'
            return result, True
        else:
            result = 'Failed'
            if len(missing_directories_for_package) > 0:
                result = result + '\n' + '\n' + 'Missing directories for package:\n' + '\n'.join(['- {}'.format(dir) for dir in missing_directories_for_package])
            if len(missing_directories_for_app) > 0:
                result = result + '\n' + '\n' + 'Missing directories for app:\n' + '\n'.join(['- {}'.format(dir) for dir in missing_directories_for_app])
            return result, False
    
    def check_project_files():
        """
        """
        missing_files_for_package = checker.missing_files(ppm.PACKAGE)
        missing_files_for_app = checker.missing_files(ppm.PACKAGE)

        if len(missing_files_for_package) == 0 or len(missing_files_for_app) == 0:
            result = 'Pass'
            return result, True
        else:
            result = 'Failed'
            if len(missing_files_for_package) > 0:
                result = result + '\n' + '\n' + 'Missing files for package:\n' + '\n'.join(['- {}'.format(file) for file in missing_files_for_package])
            if len(missing_files_for_app) > 0:
                result = result + '\n' + '\n' + 'Missing files for app:\n' + '\n'.join(['- {}'.format(file) for file in missing_files_for_app])
                
            return result, False
        
    print("Checking project structure: ", end = '')
    result, step_ok = check_project_structure()
    print(result)
    if not step_ok:
        return
    
    print("Checking project files: ", end = '')
    result, step_ok = check_project_files()
    print(result)
    if not step_ok:
        return
    
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
    parser_create.add_argument('status', choices=['package', 'app'])
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