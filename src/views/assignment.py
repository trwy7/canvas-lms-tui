import utils

def main(server: dict, course: dict, assignment: dict):
    while True:
        # Clear the screen
        utils.clear(server['name'], course['shortName'], "Assignments", assignment['title'])
        # Get page contents
        pagreq = utils.get_endpoint(assignment['url'])
        utils.printHTML(pagreq['json']['description'])
        input("Press enter to exit...")