import os
import platform
from pathlib import Path

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