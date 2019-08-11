def after_list(projects_list):
    size = {'name':0,
            'type':0,
            'venv status':0,
            'git status':0}

    for project in projects_list:
        if size['name'] < len(project['name']):
            size['name'] = len(project['name'])
        if size['type'] < len(project['type']):
            size['type'] = len(project['type'])
        if size['venv status'] < len(project['venv status']):
            size['venv status'] = len(project['venv status'])
        if size['git status'] < len(project['git status']):
            size['git status'] = len(project['git status'])

    print('{info:{width}}'.format(info='Project name', width=size['name']),        end='  ')
    print('{info:{width}}'.format(info='Type',         width=size['type']),        end='  ')
    print('{info:{width}}'.format(info='venv',         width=size['venv status']), end='  ')
    print('{info:{width}}'.format(info='git',          width=size['git status']),  end='\n')

    print('{info:-<{width}}'.format(info='', width=size['name']),        end='  ')
    print('{info:-<{width}}'.format(info='', width=size['type']),        end='  ')
    print('{info:-<{width}}'.format(info='', width=size['venv status']), end='  ')
    print('{info:-<{width}}'.format(info='', width=size['git status']),  end='\n')

    for project in projects_list:
        print('{info:{width}}'.format(info=project['name'],        width=size['name']),        end='  ')
        print('{info:{width}}'.format(info=project['type'],        width=size['type']),        end='  ')
        print('{info:{width}}'.format(info=project['venv status'], width=size['venv status']), end='  ')
        print('{info:{width}}'.format(info=project['git status'],  width=size['git status']),  end='\n')