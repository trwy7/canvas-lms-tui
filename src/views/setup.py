from InquirerPy import inquirer
import requests
import utils

def add_instance(stdscr, servers: list[dict[str,str]]):
    url = inquirer.text(message="Enter your canvas base url (including https):").execute().rstrip("/")
    while (not url.startswith("http")) or requests.get(url + "/help_links").status_code != 200:
        url = inquirer.text(message="That dosen't seem valid. Remember to include https and remove the trailing slash:").execute()
    token = inquirer.text(message="Input a canvas token. Go to " + url + "/profile/settings and generate a token. Warning: This is stored in plain text, anyone who can access your device can also access your canvas account:").execute()
    utils.set_current_instance({"name": "setup", "url": url, "token": token})
    token_test_resp = utils.get_endpoint("/api/v1/users/self")
    if token_test_resp.status_code != 200:
        token = inquirer.text(message="That token isn't working, try again:").execute()
        utils.set_current_instance({"name": "setup", "url": url, "token": token})
        token_test_resp = utils.get_endpoint("/api/v1/users/self")
    name = inquirer.text(message="Enter a name for this configuration:").execute()
    servers.append({"name": name, "url": url, "token": token})