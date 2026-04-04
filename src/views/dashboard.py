import time, sys
from InquirerPy import inquirer
from InquirerPy.base import Choice
import utils
import errors

def show_instance(server: dict[str, str]):
    # Clear the screen
    utils.clear(server['name'])
    # Let utils know we are using this instance now
    utils.set_current_instance(server)
    # Get the userinfo endpoint
    userinfo = utils.get_endpoint("/api/v1/users/self")
    if userinfo['status_code'] != 200:
        raise errors.HTTPError("Failed to get user info: " + str(userinfo.status_code))
    # Show dash sections
    tdash = inquirer.select(
        message=f"Welcome, {userinfo['json']['first_name']}! Select an option",
        choices=[
            Choice("dashboard", "Dashboard"),
            Choice("courses", "Courses")
        ],
        qmark="",
        amark=">",
        show_cursor=False
    ).execute()
    match tdash:
        case "dashboard":
            raise NotImplementedError()
        case "courses":
            raise NotImplementedError()
    time.sleep(5)