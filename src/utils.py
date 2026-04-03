import os
import platform
from pathlib import Path
import requests
import saves

cache: dict[str, str] = {}

current_instance: dict[str, str] | None = None
def get_current_instance():
    return current_instance
def set_current_instance(value: dict[str, str] | None):
    global current_instance
    current_instance = value
    return current_instance

def get_config_dir():
    home = Path.home()
    if platform.system() == "Windows":
        config_dir = Path(os.getenv("APPDATA")) / "trwy_canvas-lms-tui"
    elif platform.system() == "Darwin":
        config_dir = home / "Library" / "Application Support" / "trwy_canvas-lms-tui"
    else:
        config_dir = Path(os.getenv("XDG_CONFIG_HOME", home / ".config")) / "trwy_canvas-lms-tui"
        
    # Create the directory if it doesn't exist
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir

def get_endpoint(endpoint, **kwargs):
    if current_instance is None:
        raise RuntimeError("get_endpoint was called before an instance was assigned")
    return requests.get(current_instance['url'] + endpoint, headers={"Authorization": "Bearer " + current_instance['token']}, timeout=10, allow_redirects=True, **kwargs)
