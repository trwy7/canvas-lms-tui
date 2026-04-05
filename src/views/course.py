
from InquirerPy import inquirer
from InquirerPy.base import Choice
import utils
import views.modules
import views.assignments

def main(server: dict, course: dict):
    while True:
        # Clear the screen
        utils.clear(server['name'], course['shortName'])
        # Show dash sections
        tdash = inquirer.select(
            message="Select an option",
            choices=[
                Choice("modules", "Modules"),
                Choice("grades", "Grades"),
                Choice("assignments", "Assignments"),
                Choice("announcements", "Announcements"),
                Choice("back", "Back")
            ],
            qmark="",
            amark=">",
            show_cursor=False
        ).execute()
        match tdash:
            case "modules":
                views.modules.main(server, course)
            case "grades":
                raise NotImplementedError()
            case "assignments":
                views.assignments.main(server, course)
            case "announcements":
                raise NotImplementedError()
            case "back":
                break