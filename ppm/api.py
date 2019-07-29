import os
import ppm
import ppm.exceptions


def create_package(name):
    raise ppm.exceptions.NotYetImplementedException

def create_app(name):
    raise ppm.exceptions.NotYetImplementedException

def list():
    ret_val = []
    for project in os.listdir(ppm.python_projects_path):
        ret_val.append({"name":project,
                        "type":"Not yet implemented",
                        "coherency check":"Not yet implemented",
                        "last commit":"Not yet implemented"})
    return ret_val

def report(name):
    raise ppm.exceptions.NotYetImplementedException

def develop(program, name):
    raise ppm.exceptions.NotYetImplementedException