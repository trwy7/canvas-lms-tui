
from InquirerPy import inquirer
from InquirerPy.base import Choice
import utils
import errors
import views.course

def main(server: dict, course: dict):
    while True:
        # Clear the screen
        utils.clear(server['name'], course['shortName'], "Modules")
        # Get modules
        modreq = utils.get_endpoint(f"/api/v1/courses/{course['id']}/modules")
        if modreq['status_code'] != 200:
            raise errors.HTTPError("Failed to get course modules: Error " + str(modreq['status_code']))
        choices = [
            Choice(
                module,
                f"{module['name']} ({module['items_count']})"
            )
            for module in modreq['json']
        ]
        choices.append(Choice("back", "Back"))
        # Show courses
        module = inquirer.select(
            message="Select a module",
            choices=choices,
            qmark="",
            amark=">",
            show_cursor=False
        ).execute()
        if module == "back":
            break
        views.module.main(server, course, module)