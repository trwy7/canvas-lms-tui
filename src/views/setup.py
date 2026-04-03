from InquirerPy import inquirer
import requests
import utils

def add_instance(servers: list[dict[str,str]]):
    utils.clear("CanvasTUI setup")
    url = inquirer.text(message="Enter your canvas base url (including https):").execute().rstrip("/")
    while (not url.startswith("http")) or requests.get(url + "/help_links").status_code != 200:
        url = inquirer.text(message="That dosen't seem valid. Remember to include https and remove the trailing slash:").execute()
    utils.set_current_instance({"name": "setup", "url": url, "token": ""})
    token, token_test_resp = utils.request_token(url)
    name = inquirer.text(message=f"Hello, {token_test_resp.json()['first_name']}! Enter a name for this configuration:").execute()
    servers.append({"name": name, "url": url, "token": token})

