
from InquirerPy import inquirer
from InquirerPy.base import Choice
import utils
import views.course

def main(server: dict):
    # Clear the screen
    utils.clear(server['name'], "Dashboard")
    # Get dashboard cards # TODO: Get list of assignments due today
    courses = utils.get_endpoint("/api/v1/dashboard/dashboard_cards")['json']
    # Show courses
    course = inquirer.select(
        message="Select an option",
        choices=[
            Choice(
                course,
                course['shortName']
            )
            for course in courses
        ],
        qmark="",
        amark=">",
        show_cursor=False
    ).execute()
    views.course.main(server, course)