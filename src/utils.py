import os
import locale
from datetime import datetime, timedelta
from typing import Literal, Any
import html2text
from rich.console import Console
from babel import Locale
from rich.markdown import Markdown
from InquirerPy import inquirer
import requests
import saves

req_cache: dict[str, str] = saves.load_data("cache.json", {"timestamp": datetime.now().timestamp()})
if req_cache['timestamp'] > (datetime.now() + timedelta(hours=2)).timestamp():
    req_cache = {"timestamp": datetime.now().timestamp()}

htt = html2text.HTML2Text(bodywidth=0)
console = Console()

try:
    loc = Locale.default()
except:
    try:
        loc = Locale.parse(locale.getdefaultlocale()[0])
    except:
        loc = Locale.parse('en_US')

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
    value['token'] = value['token'].strip("\n ") # Weird but sometimes json seems to bug
    current_instance = value
    return current_instance

def clear(*titles):
    os.system('cls' if os.name == 'nt' else 'clear')
    if titles:
        title = "\x1b[0;36;7m/" + "/".join(titles) + "\x1b[0m"
    else:
        title = "\x1b[0;7m" + "_CanvasTUI_" + "\x1b[0m"
    print(title + '\n')

def printHTML(html):
    console.print(Markdown(htt.handle(html))) # really jank but works

def request_token(url):
    token = inquirer.secret(message="Input a personal canvas token. Go to " + url + "/profile/settings and generate a token. Warning: This is stored in plain text, anyone who can access your device may be able to access your canvas account:").execute()
    current_instance['token'] = token.strip("\n ")
    token_test_resp = get_endpoint("/api/v1/users/self", check_token=False, use_cache=False)
    if token_test_resp['status_code'] != 200:
        token = inquirer.secret(message="That token isn't working, try again:").execute()
        current_instance['token'] = token
        token_test_resp = get_endpoint("/api/v1/users/self", check_token=False, use_cache=False)
    return token, token_test_resp

def get_endpoint(endpoint, check_token=True, use_cache=True) -> dict[Literal["status_code", "json"], Any]:
    cache_key = current_instance['name'] + "/" + current_instance['url'] + endpoint
    if use_cache and cache_key in req_cache and req_cache[cache_key]['timestamp'] > (datetime.now() - timedelta(minutes=5)).timestamp():
        return req_cache[cache_key]
    if current_instance is None:
        raise RuntimeError("get_endpoint was called before an instance was assigned")
    if endpoint.startswith("http"):
        rurl = endpoint # scary, do not pass arbitrary values into this function
    else:
        rurl = current_instance['url'] + endpoint
    r = requests.get(rurl, headers={"Authorization": "Bearer " + current_instance['token']}, timeout=10, allow_redirects=True)
    if check_token and r.status_code == 401:
        print(f"{colors.RED}{colors.BOLD}The canvas token provided has expired. Please get another one.{colors.END}")
        current_instance['token'] = request_token(current_instance['url'])[0]
        r = requests.get(current_instance['url'] + endpoint, headers={"Authorization": "Bearer " + current_instance['token']}, timeout=10, allow_redirects=True)
    jresp = {
        'status_code': r.status_code,
        'json': r.json() if r.text else None,
        'timestamp': datetime.now().timestamp()
    }
    if use_cache:
        req_cache[cache_key] = jresp
    return jresp

def clear_request_cache():
    global req_cache
    req_cache = {"timestamp": datetime.now().timestamp()}

def on_exit():
    saves.save_data("cache.json", req_cache)