import os
import json
from utils import get_config_dir

CONFIG_DIR = get_config_dir()

def save_data(file: str, data):
    """Saves json data to a file

    Args:
        file (str): The file name
        data (Any): The data to save
    """
    fpath = str(CONFIG_DIR / file)
    with open(fpath, "w", encoding="UTF-8") as f:
        json.dump(data, f, indent=2)
    os.chmod(fpath, 0o600)

def load_data(file: str, default=None):
    """Loads data from a config file

    Args:
        file (str): The file name
        default (Any, optional): Loads the config. Defaults to None.

    Returns:
        Any: The JSON or the default if it was not found
    """
    fpath = str(CONFIG_DIR / file)
    if os.path.exists(fpath):
        with open(fpath, "r", encoding="UTF-8") as f:
            return json.load(f)
    return default
