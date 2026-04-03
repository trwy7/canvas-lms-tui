import pip_system_certs.wrapt_requests # PYInstaller
pip_system_certs.wrapt_requests.inject_truststore() # PYInstaller
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header
import saves

def init():
    servers = saves.load_data("servers.json", [])
    if len(servers) == 0:
        add_instance(servers) # TODO: add
        saves.save_data("servers.json", servers)
    elif len(servers) == 1:
        show_instance(servers[0]) # TODO: add
    instance_select(servers) # TODO: add

if __name__ == "__main__":
    init()