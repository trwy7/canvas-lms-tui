
from InquirerPy import inquirer
from InquirerPy.base import Choice
import utils

def main(server: dict, course: dict):
    # Clear the screen
    utils.clear(server['name'], course['shortName'])
    # Show dash sections
    tdash = inquirer.select(
        message="Select an option",
        choices=[
            Choice("modules", "Modules"),
            Choice("grades", "Grades"),
            Choice("assignments", "Assignments"),
            Choice("announcements", "Announcements")
        ],
        qmark="",
        amark=">",
        show_cursor=False
    ).execute()
    match tdash:
        case "modules":
            raise NotImplementedError()
        case "grades":
            raise NotImplementedError()
        case "assignments":
            raise NotImplementedError()
        case "announcements":
            raise NotImplementedError()