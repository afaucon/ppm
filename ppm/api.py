import os
import ppm


def create_package(name):
    pass

def create_app(name):
    pass

def list():
    ret_val = []
    for project in os.listdir(ppm.python_projects_path):
        ret_val.append({"name":project,
                        "type":"Not yet implemented",
                        "coherency check":"Not yet implemented",
                        "last commit":"Not yet implemented"})
    return ret_val

def report(name):
    return "hello, world!"

def develop(program, name):
    pass