import curses
import pip_system_certs.wrapt_requests # PYInstaller
pip_system_certs.wrapt_requests.inject_truststore() # PYInstaller
import saves
from views.setup import add_instance
import curses

def init(stdscr: curses.window):
    # Clear the screen
    stdscr.clear()
    # Get the configured servers
    servers = saves.load_data("servers.json", [])
    if len(servers) == 0:
        # Let's add one!
        add_instance(stdscr, servers) # TODO: add
        saves.save_data("servers.json", servers)
    if len(servers) == 1:
        # Use it as a default
        show_instance(stdscr, servers[0]) # TODO: add
    # Ask the user for a selection
    instance_select(stdscr, servers) # TODO: add

if __name__ == "__main__":
    curses.wrapper(init)