import ppm


def check_project_structure(checker):
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

def check_project_files(checker):
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