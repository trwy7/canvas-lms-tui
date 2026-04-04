from InquirerPy import inquirer
from InquirerPy.base import Choice
import utils
import errors
import views.page
import views.assignment

def main(server: dict, course: dict, module: dict):
    while True:
        # Clear the screen
        utils.clear(server['name'], course['shortName'], "Modules", module['name'])
        # Get module contents
        modreq = utils.get_endpoint(module['items_url'])
        if modreq['status_code'] != 200:
            raise errors.HTTPError("Failed to get module: Error " + str(modreq['status_code']))
        choices = [
            Choice(
                item,
                '-' * item['indent'] + f"{item['title']} ({item['type']})"
            )
            for item in modreq['json']
        ]
        choices.append(Choice("back", "Back"))
        # Show courses
        item = inquirer.select(
            message="Select an item",
            choices=choices,
            qmark="",
            amark=">",
            show_cursor=False
        ).execute()
        if item == "back":
            break
        match item['type']:
            case "SubHeader":
                pass
            case "Page":
                views.page.main(server, course, item)
            case "Assignment":
                views.assignment.main(server, course, item)
            case _:
                raise NotImplementedError(f"Type \"{item['type']}\" is not known")