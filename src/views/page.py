import utils
import errors

def main(server: dict, course: dict, page: dict):
    # Clear the screen
    utils.clear(server['name'], course['shortName'], "Pages", page['title'])
    # Get page contents
    pagreq = utils.get_endpoint(page['url'])
    if pagreq['status_code'] != 200:
        raise errors.HTTPError("Failed to get page: Error " + str(pagreq['status_code']))
    utils.printHTML(pagreq['json']['body'])
    input("Press enter to exit...")