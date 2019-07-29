def after_create_package(message):
    print(message)

def after_create_app(message):
    print(message)

def after_list(projects_list):
    size = {"name":0,
            "type":0,
            "coherency check":0,
            "last commit":0}
    for project in projects_list:
        if size["name"] < len(project['name']):
            size["name"] = len(project['name'])
        if size["type"] < len(project['type']):
            size["type"] = len(project['type'])
        if size["coherency check"] < len(project['coherency check']):
            size["coherency check"] = len(project['coherency check'])
        if size["last commit"] < len(project['last commit']):
            size["last commit"] = len(project['last commit'])

    print('{info:{width}}'.format(info='Project name',    width=size['name']),            end=' ')
    print('{info:{width}}'.format(info='Type',            width=size['type']),            end=' ')
    print('{info:{width}}'.format(info='Coherency check', width=size['coherency check']), end=' ')
    print('{info:{width}}'.format(info='Last commit',     width=size['last commit']),     end='\n')

    print('{info:-<{width}}'.format(info='', width=size['name']),            end=' ')
    print('{info:-<{width}}'.format(info='', width=size['type']),            end=' ')
    print('{info:-<{width}}'.format(info='', width=size['coherency check']), end=' ')
    print('{info:-<{width}}'.format(info='', width=size['last commit']),     end='\n')

    for project in projects_list:
        print('{info:{width}}'.format(info=project['name'],            width=size['name']),            end=' ')
        print('{info:{width}}'.format(info=project['type'],            width=size['type']),            end=' ')
        print('{info:{width}}'.format(info=project['coherency check'], width=size['coherency check']), end=' ')
        print('{info:{width}}'.format(info=project['last commit'],     width=size['last commit']),     end='\n')
        
def after_check(report):
    print("Report display not yet implemented")

def after_develop():
    pass