from InquirerPy import inquirer
from InquirerPy.base import Choice
import utils
import views.assignment

def main(server: dict, course: dict):
    while True:
        # Clear the screen
        utils.clear(server['name'], course['shortName'], "Assignments")
        # Get assignments
        agreq = utils.get_endpoint(f"/api/v1/courses/{course['id']}/assignments")
        assignments = agreq['json']
        choices = [
            Choice(assignment, assignment['name'])
            for assignment in assignments
        ]
        choices.append(Choice("back", "Back"))
        selected = inquirer.fuzzy(
            message="Select an assignment",
            choices=choices,
            qmark="",
            amark=">",
            border=True,
            info=True
        ).execute()
        if selected == "back":
            break
        views.assignment.main(server, course, selected)