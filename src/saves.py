import os
import json
import platform
from pathlib import Path

# Get the home directory
home = Path.home()
# Find the config dir we should be using
if platform.system() == "Windows":
    CONFIG_DIR = Path(os.getenv("APPDATA")) / "trwy_canvas-lms-tui"
elif platform.system() == "Darwin":
    CONFIG_DIR = home / "Library" / "Application Support" / "trwy_canvas-lms-tui"
else:
    CONFIG_DIR = Path(os.getenv("XDG_CONFIG_HOME", home / ".config")) / "trwy_canvas-lms-tui"
    
# Create the directory if it doesn't exist
CONFIG_DIR.mkdir(parents=True, exist_ok=True)

def save_data(file: str, data):
    """Saves json data to a file

    Args:
        file (str): The file name
        data (Any): The data to save
    """
    fpath = str(CONFIG_DIR / file)
    with open(fpath, "w", encoding="UTF-8") as f:
        json.dump(data, f)
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
