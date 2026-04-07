from InquirerPy import inquirer
from InquirerPy.base import Choice
import utils

def main(server: dict, course: dict):
    while True:
        # Clear the screen
        utils.clear(server['name'], course['shortName'], "Assignments")
        # Get announcements
        anreq = utils.get_endpoint(f"/api/v1/announcements?context_codes[]=course_{course['id']}") # why is this so weird
        announcements = anreq['json']
        if announcements is None:
            print("There are no announcements, or you do not have access to view any\n")
            input("Press enter to go back...")
        choices = [
            Choice(announcement, announcement['title'])
            for announcement in announcements
        ]
        choices.append(Choice("back", "Back"))
        selected = inquirer.fuzzy(
            message="Select an announcement",
            choices=choices,
            qmark="",
            amark=">",
            border=True,
            info=True
        ).execute()
        if selected == "back":
            break
        view_announcement(server, course, selected)

def view_announcement(server, course, announcement):
    # Clear the screen
    utils.clear(server['name'], course['shortName'], "Announcements", announcement['title'])
    # Get page contents
    utils.printHTML(announcement['message'])
    input("Press enter to exit...")