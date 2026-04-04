
from InquirerPy import inquirer
from InquirerPy.base import Choice
import utils
import views.course

def main(server: dict):
    while True:
        # Clear the screen
        utils.clear(server['name'], "Dashboard")
        # Get dashboard cards # TODO: Get list of assignments due today
        courses = utils.get_endpoint("/api/v1/dashboard/dashboard_cards")['json']
        choices = [
            Choice(
                course,
                course['shortName']
            )
            for course in courses
        ]
        choices.append(Choice("back", "Back"))
        # Show courses
        course = inquirer.select(
            message="Select a course",
            choices=choices,
            qmark="",
            amark=">",
            show_cursor=False
        ).execute()
        if course == "back":
            break
        views.course.main(server, course)