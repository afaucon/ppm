import os
import subprocess
import ppm
import ppm.project
import ppm.checker


def create_package(project_name, package_name, description, url, author, author_email):
    package = ppm.project.Package(project_name, package_name, description, url, author, author_email)
    package.create()
    #raise ppm.exceptions.NotYetImplementedException

def create_app(project_name, app_name, description, url, author, author_email):
    app = ppm.project.App(project_name, app_name, description, url, author, author_email)
    app.create()
    #raise ppm.exceptions.NotYetImplementedException

def list():
    ret_val = []
    for project_name in os.listdir(ppm.python_projects_path):
        ret_val.append({'name':project_name,
                        'type':ppm.checker.Checker(project_name).get_project_type(),
                        'venv status':ppm.checker.Checker(project_name).get_venv_status(),
                        'git status':ppm.checker.Checker(project_name).get_git_status()})
    return ret_val

def open_visual_studio_code(project_name):
    project_path = ppm.python_projects_path / project_name
    if not os.path.isdir(project_path):
        raise ppm.exceptions.ProjectDoesNotExist
    subprocess.run(["Code", "."], cwd=project_path, shell=True)