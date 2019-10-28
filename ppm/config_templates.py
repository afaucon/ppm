import json
import logging


CONFIG_FILE = ".ppm"


class BookmarkedTemplates:
    """
    Description to write
    """

    def __init__(self):
        """
        Main constructor
        """
        self.config_found = False
        self.config = None
        
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                new_config_file = False
        except FileNotFoundError:
            config = {}
            new_config_file = True
        except:
            logging.error("An unexpected error occured when trying to read from the config file.")
            raise

def add_template(git_template):
    """
    Adds a git template into the bookmarked templates.
    """
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
            new_config_file = False
    except FileNotFoundError:
        config = {}
        new_config_file = True
    except:
        logging.error("An unexpected error occured when trying to read from the config file.")
        raise


    if 'bookmarked_templates' in config and git_template in config['bookmarked_templates']:
        logging.warning("Config file not updated because item is already stored.")
    else:

        if 'bookmarked_templates' not in config:
            config['bookmarked_templates'] = [git_template]
        else:
            config['bookmarked_templates'].append(git_template)

        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(config, f)
        except:
            logging.error("An unexpected error occured when trying to write in the config file.")
            raise
        else:
            if new_config_file:
                logging.info("Config file created.")
            else:
                logging.info("Config file updated.")

def remove_template(git_template):
    """
    Removes a git template from the bookmarked templates.
    """
    config = {}
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        logging.warning("No existing config file.")
    except:
        logging.error("An unexpected error occured when trying to read from the config file.")
        raise
    else:
        if 'bookmarked_templates' not in config or git_template not in config['bookmarked_templates']:
            logging.warning("Config file not updated because item not found.")
        else:

            config['bookmarked_templates'].remove(git_template)

            try:
                with open(CONFIG_FILE, 'w') as f:
                    json.dump(config, f)
            except:
                logging.error("An unexpected error occured when trying to write in the config file.")
                raise
            else:
                logging.info("Config file updated.")

def get_templates():
    """
    Returns the bookmarked templates.
    """
    config = {}
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        logging.info("No existing config file.")
        return []
    except:
        logging.error("An unexpected error occured when trying to read from the config file.")
        raise
    else:
        if 'bookmarked_templates' in config:
            return config['bookmarked_templates']
        else:
            return []