from InquirerPy import inquirer
from InquirerPy.base import Choice
import utils
import views.modules
import views.assignments
import views.announcements
import views.grades

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
                views.grades.main(server, course)
            case "assignments":
                views.assignments.main(server, course)
            case "announcements":
                views.announcements.main(server, course)
            case "back":
                break