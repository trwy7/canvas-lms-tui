from InquirerPy import inquirer
from InquirerPy.base import Choice
from datetime import datetime
from babel.dates import format_datetime
import utils
import requests

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
        messages = utils.get_endpoint("/api/v1/conversations/" + str(message['id']) + "?auto_mark_as_read=true")['json']
        # Reverse into newest last
        messages['messages'].reverse()
        # Print messages
        participant_nmap = {u['id']: u['name'] for u in messages['participants']} # Author names are not included in the message for some reason
        for rmessage in messages['messages']:
            print(participant_nmap[rmessage['author_id']] + " at " + format_datetime(datetime.fromisoformat(rmessage['created_at'])) + ":")
            print(rmessage['body'] + "\n")
        # We cannot mark as read for individual messages for some reason, if someone finds a way, make an issue!
        # Show messages
        sel = inquirer.select(
            message="Select an option",
            choices=[
                Choice("reply", "Reply"),
                Choice("back", "Back")
            ],
            qmark="",
            amark=">",
            show_cursor=False
        ).execute()
        match sel:
            case "back":
                break
            case "reply":
                reply_to_msg(server, message)

def reply_to_msg(server: dict, message: dict):
    # Request message
    cmt = inquirer.text(
        message="Enter reply text:",
        multiline=True,
    ).execute()
    # Confirm
    conf = inquirer.confirm(
        message="Are you sure you want to send this message"
    ).execute()
    if not conf:
        return
    # Add it!
    t = requests.post(f"{server['url']}/api/v1/conversations/{message['id']}/add_message", params={"body": cmt}, headers={"Authorization": f"Bearer {server['token']}"}, timeout=20)
    if t.status_code != 200:
        input("Request may have failed: " + str(t.status_code))
    utils.clear_request_cache()