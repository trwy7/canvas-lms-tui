from InquirerPy import inquirer
from InquirerPy.base import Choice
from views.setup import add_instance
from views.dashboard import show_instance
import utils
import saves

def instance_select(servers: dict):
    while True:
        # Clear the screen
        utils.clear()
        # Get choices
        choices = [
            Choice(server, server['name']) for server in servers
        ]
        choices.append(Choice("new", "Add instance"))
        # Pick an instance
        server = inquirer.select(
            message="Select an instance",
            choices=choices,
            qmark="",
            amark=">",
            show_cursor=False
        ).execute()
        # Show it
        if server == "new":
            add_instance(servers)
            saves.save_data("servers.json", servers)
        else:
            show_instance(server)
