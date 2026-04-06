import pip_system_certs.wrapt_requests # PYInstaller
pip_system_certs.wrapt_requests.inject_truststore() # PYInstaller
import sys
import saves
from views.setup import add_instance
from views.dashboard import show_instance
from views.servers import instance_select
import utils

# Get the configured servers
servers = saves.load_data("servers.json", [])

def init():
    # Clear the screen
    utils.clear()
    if len(servers) == 0:
        # Let's add one!
        add_instance(servers)
        saves.save_data("servers.json", servers)
    if len(servers) == 1:
        # Use it as a default
        show_instance(servers[0])
    # Ask the user for a selection
    instance_select(servers)

if __name__ == "__main__":
    try:
        sys.stdout.write("\033[?1049h\033[H")
        sys.stdout.flush()
        print("Launching!")
        init()
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write("\033[?1049l")
        sys.stdout.flush()
        saves.save_data("servers.json", servers)
        utils.on_exit() # Save the cache