import os
import subprocess
import ppm
import ppm.exceptions
import ppm.checker


def create_package(project_name):
    raise ppm.exceptions.NotYetImplementedException

def create_app(project_name):
    raise ppm.exceptions.NotYetImplementedException

def list():
    ret_val = []
    for project_name in os.listdir(ppm.python_projects_path):
        ret_val.append({'name':project_name,
                        'type':ppm.checker.Checker(project_name).get_project_type(),
                        'venv status':ppm.checker.Checker(project_name).get_venv_status(),
                        'git status':ppm.checker.Checker(project_name).get_git_status()})
    return ret_val

def develop(program, project_name):
    subprocess.run(["Code", "."], cwd=ppm.python_projects_path / project_name, shell=True)