import html2text
from rich.console import Console
from rich.markdown import Markdown
import utils
import errors

console = Console()

def main(server: dict, course: dict, page: dict):
    # Clear the screen
    utils.clear(server['name'], course['shortName'], "Pages", page['title'])
    # Get page contents
    pagreq = utils.get_endpoint(page['url'])
    if pagreq['status_code'] != 200:
        raise errors.HTTPError("Failed to get page: Error " + str(pagreq['status_code']))
    console.print(html2text.html2text(pagreq['json']['body'])) # really jank but works
    input("Press enter to exit...")