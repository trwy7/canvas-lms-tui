from InquirerPy import inquirer
from InquirerPy.base import Choice
from datetime import datetime
from babel.dates import format_datetime
import utils

def main(server: dict):
    while True:
        # Clear the screen
        utils.clear(server['name'], "Inbox")
        # Get messages
        messages = utils.get_endpoint("/api/v1/conversations")['json']
        choices = [
            Choice(
                message,
               f"{message['subject']} - {", ".join([p['name'] for p in message['participants']])}"
            )
            for message in messages
        ]
        choices.append(Choice("back", "Back"))
        # Show messages
        message = inquirer.fuzzy(
            message="Select a message",
            choices=choices,
            qmark="",
            amark=">",
            border=True
        ).execute()
        if message == "back":
            break
        view_message(server, message)

def view_message(server: dict, message: dict):
    while True:
        # Clear the screen
        utils.clear(server['name'], "Inbox", message['subject'])
        # Get message 
        messages = utils.get_endpoint("/api/v1/conversations/" + str(message['id']))['json']
        participant_nmap = {u['id']: u['name'] for u in messages['participants']}
        for message in messages['messages']:
            print(participant_nmap[message['author_id']] + " at " + format_datetime(datetime.fromisoformat(message['created_at'])) + ":")
            print(message['body'] + "\n")
        # We cannot mark as read for individual messages for some reason, if someone finds a way, make an issue!
        # Show messages
        message = inquirer.select(
            message="Select a message",
            choices=[
                Choice("reply", "Reply"),
                Choice("back", "Back")
            ],
            qmark="",
            amark=">",
            show_cursor=False
        ).execute()
        match message:
            case "back":
                break
            case "back":
                pass