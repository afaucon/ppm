import chardet
import re
import os


def files_are_compilant(instance, template):
    '''
    This function returns true if the instance and the template are compliant.
    Otherwise, it returns false and the string reason why they are not compliant.
    '''

    # Detect the likely encoding of the template
    with open(template, 'rb') as f:
        rawdata = f.read()
        template_likely_encoding = chardet.detect(rawdata)

    # Open the template with the detected encoding
    with open(template, encoding=template_likely_encoding['encoding']) as f:
        template_content = f.read()
    
    # Define the regex:  {{ var_name }}
    regex = r"(?<=\{\{).*?(?=\}\})"

    # Get all the matches in an iterable object
    matches = re.finditer(regex, template_content, re.DOTALL)

    # Construct the template constraints
    template_constraints = []
    constr_start_pos = 0
    for _, match in enumerate(matches, start=1):
        constr_stop_pos = match.start() - 2  # -2 because there is the '{{' in front of the match
        template_constraints.append( template_content[constr_start_pos : constr_stop_pos] )
        constr_start_pos = match.end() + 2   # -2 because there is the '}}' after the match
    constr_stop_pos = len(template_content)
    template_constraints.append( template_content[constr_start_pos : constr_stop_pos] )

    # Detect the likely encoding of the template
    with open(instance, 'rb') as f:
        rawdata = f.read()
        instance_likely_encoding = chardet.detect(rawdata)

    # Check that the encoding of the instance and the template are the same
    if instance_likely_encoding['encoding'] != template_likely_encoding['encoding']:
        return False, 'Encodings are different: {}/{}'.format(instance_likely_encoding['encoding'], template_likely_encoding['encoding'])

    # Open the instance
    with open(instance, encoding='utf-8') as f:
        string = f.read()

    # Check that all the template constraints are in the instance
    current_position = 0  # Start from the beginning of the file
    for template_constraint in template_constraints:

        match_position = string.find(template_constraint, current_position)
        if match_position == -1:
            return False, 'Template constraints are not satisfied'
        else:
            current_position = match_position
    
    return True, ''

def directories_are_compilant(instance, template):
    '''
    This function returns true if the instance and the template are compliant.
    Otherwise, it returns false and a list of the uncompliance.
    '''

    uncompliances = []
    for root, dirs, files in os.walk(template):
        if os.path.join(template, '.git') not in root:
            
            # Checking that all directories of the template also exist in instance
            for dirname in dirs:
                template_fullpath = os.path.join(root, dirname)
                relpath = os.path.relpath(template_fullpath, template)
                instance_fullpath = os.path.join(instance, relpath)
                if not os.path.isdir(instance_fullpath):
                    uncompliances.append( {
                        'type'   : 'directory',
                        'relpath': relpath,
                        'reason' : 'missing directory'
                    } )

            # Checking that all files of the template also exist in instance
            for filename in files:
                template_fullpath = os.path.join(root, filename)
                relpath = os.path.relpath(template_fullpath, template)
                instance_fullpath = os.path.join(instance, relpath)
                if not os.path.isfile(instance_fullpath):
                    uncompliances.append( {
                        'type'   : 'file',
                        'relpath': relpath,
                        'reason' : 'missing file'
                    } )
                else:
                    result, reason = files_are_compilant(instance_fullpath, template_fullpath)
                    if not result:
                        uncompliances.append( {
                            'type'   : 'file',
                            'relpath': relpath,
                            'reason' : reason
                        } )

    return len(uncompliances) == 0, uncompliances