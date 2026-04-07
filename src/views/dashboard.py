from InquirerPy import inquirer
from InquirerPy.base import Choice
import utils
import errors
import views.courses
import views.inbox

def show_instance(server: dict[str, str]):
    while True:
        # Clear the screen
        utils.clear(server['name'])
        # Let utils know we are using this instance now
        utils.set_current_instance(server)
        # Get the userinfo endpoint
        userinfo = utils.get_endpoint("/api/v1/users/self")
        if userinfo['status_code'] != 200:
            raise errors.HTTPError("Failed to get user info: " + str(userinfo.status_code))
        unread_count = utils.get_endpoint("/api/v1/conversations/unread_count")
        if unread_count['status_code'] != 200:
            print("Failed to get unread message count\n")
            unread_count = 0
        else:
            unread_count = int(unread_count['json']['unread_count'])
        # Show dash sections
        tdash = inquirer.select(
            message=f"Welcome, {userinfo['json']['first_name']}! Select an option",
            choices=[
                Choice("dashboard", "Dashboard"),
                Choice("inbox", "Messages" + (f" ({unread_count})" if unread_count else "")),
                Choice("recache", "Delete cache"),
                Choice("changeinstance", "Switch instances")
            ],
            qmark="",
            amark=">",
            show_cursor=False
        ).execute()
        match tdash:
            case "dashboard":
                views.courses.main(server)
            case "inbox":
                views.inbox.main(server)
            case "recache":
                utils.clear_request_cache()
            case "changeinstance":
                break