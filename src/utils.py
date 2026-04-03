import os
import platform
from pathlib import Path
from InquirerPy import inquirer
import requests

req_cache: dict[str, str] = {}

class colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    END = '\033[0m'
    UNDERLINE = '\033[4m'
    OVERLINE = '\033[53m'
    ITALIC = '\033[3m'
    BOLD = '\033[1m'

current_instance: dict[str, str] | None = None
def get_current_instance():
    return current_instance
def set_current_instance(value: dict[str, str] | None):
    global current_instance
    current_instance = value
    current_instance["id"] = value['token'].split("~")[0]
    return current_instance

def clear(*titles):
    os.system('cls' if os.name == 'nt' else 'clear')
    if titles:
        title = "/" + "/".join(titles)
    else:
        title = "---CanvasTUI---"
    print(title + '\n')

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

def request_token(url):
    token = inquirer.text(message="Input a canvas token. Go to " + url + "/profile/settings and generate a token. Warning: This is stored in plain text, anyone who can access your device can also access your canvas account:").execute()
    current_instance['token'] = token
    token_test_resp = get_endpoint("/api/v1/users/self", check_token=False)
    if token_test_resp.status_code != 200:
        token = inquirer.text(message="That token isn't working, try again:").execute()
        current_instance['token'] = token
        token_test_resp = get_endpoint("/api/v1/users/self", check_token=False)
    return token, token_test_resp

def get_endpoint(endpoint, check_token=True):
    # TODO: add a cache to this function
    if current_instance is None:
        raise RuntimeError("get_endpoint was called before an instance was assigned")
    r = requests.get(current_instance['url'] + endpoint, headers={"Authorization": "Bearer " + current_instance['token']}, timeout=10, allow_redirects=True)
    if check_token and r.status_code == 401:
        print(f"{colors.RED}{colors.BOLD}The canvas token provided has expired. Please get another one.{colors.END}")
        current_instance['token'] = request_token(current_instance['url'])[0]
        r = requests.get(current_instance['url'] + endpoint, headers={"Authorization": "Bearer " + current_instance['token']}, timeout=10, allow_redirects=True)
    return r
