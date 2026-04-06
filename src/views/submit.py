from InquirerPy import inquirer
from InquirerPy.base import Choice
from InquirerPy.validator import PathValidator
import utils
import requests
import os

def main(server: dict, course: dict, assignment: dict):
    # Clear the screen
    utils.clear(server['name'], course['shortName'], "Assignments", assignment['name'], "Submit")
    # Get valid choices
    choices = []
    if "online_text_entry" in assignment['submission_types']:
        choices.append(Choice("text", "Text entry"))
    if "online_url" in assignment['submission_types']:
        choices.append(Choice("url", "Website URL"))
    if "online_upload" in assignment['submission_types']:
        choices.append(Choice("file", "Upload file"))
    choices.append(Choice("back", "Back"))
    # Ask for input
    item = inquirer.select(
        message="Select a submission type",
        choices=choices,
        qmark="",
        amark=">",
        show_cursor=False
    ).execute()
    match item:
        case "text":
            text_submit(server, course, assignment)
        case "url":
            url_submit(server, course, assignment)
        case "file":
            file_submit(server, course, assignment)

def file_submit(server: dict, course: dict, assignment: dict):
    # Clear the screen
    utils.clear(server['name'], course['shortName'], "Assignments", assignment['name'], "Submit", "File upload")
    # Get the file(s)
    flist = []
    choice = inquirer.select(
        message="Select an option",
        choices=[
            Choice("add", "Add file"),
            Choice("submit", "Submit!"),
            Choice("cancel", "Cancel")
        ],
        qmark="",
        amark=">",
        show_cursor=False
    ).execute()
    while choice == "add":
        try:
            flist.append(inquirer.filepath(
                message="Enter file to upload",
                default=os.path.expanduser("~"),
                validate=PathValidator(is_file=True, message="You must pick a file")
            ).execute())
        except KeyboardInterrupt:
            pass
        utils.clear(server['name'], course['shortName'], "Assignments", assignment['name'], "Submit", "File upload")
        print("Submitting:\n- " + "\n- ".join(flist) + "\n")
        choice = inquirer.select(
            message="Select an option",
            choices=[
                Choice("add", "Add file"),
                Choice("submit", "Submit!"),
                Choice("cancel", "Cancel")
            ],
            qmark="",
            amark=">",
            show_cursor=False
        ).execute()
    if choice == "cancel":
        return
    # Confirm one last time
    conf = inquirer.confirm(
        message="Are you sure you want to submit"
    ).execute()
    if not conf:
        return
    # Submit it!
    utils.clear(server['name'], course['shortName'], "Assignments", assignment['name'], "Submit", "File upload", "Submitting")
    upload_ids = []
    for file in flist:
        fname = os.path.basename(file)
        upl = requests.post(
            f"{server['url']}/api/v1/courses/{course['id']}/assignments/{assignment['id']}/submissions/self/files",
            params={"size": os.path.getsize(file), "name": fname},
            headers={"Authorization": f"Bearer {server['token']}"},
            timeout=10
        )
        upl_url = upl.json()
        print(upl_url)
        # TODO: Finish
        input()

def text_submit(server: dict, course: dict, assignment: dict):
    # Clear the screen
    utils.clear(server['name'], course['shortName'], "Assignments", assignment['name'], "Submit", "Text entry")
    # Ask for input
    resp = inquirer.text(
        message="Enter submission text (HTML)",
        qmark="",
        amark=">",
        multiline=True
    ).execute()
    # Confirm
    conf = inquirer.confirm(
        message="Are you sure you want to submit"
    ).execute()
    if not conf:
        return
    # Submit!
    upl = requests.post(
        f"{server['url']}/api/v1/courses/{course['id']}/assignments/{assignment['id']}/submissions",
        params={"submission[submission_type]": "online_text_entry", "submission[body]": resp},
        headers={"Authorization": f"Bearer {server['token']}"},
        timeout=10
    )
    if upl.status_code != 201:
        print("Submission may have failed:")
        print(str(upl))
        print(str(upl.status_code))
        input(str(upl.text))
    utils.clear_request_cache()

def url_submit(server: dict, course: dict, assignment: dict):
    # Clear the screen
    utils.clear(server['name'], course['shortName'], "Assignments", assignment['name'], "Submit", "URL")
    # Ask for input
    resp = inquirer.text(
        message="Enter submission URL",
        qmark="",
        amark=">"
    ).execute()
    # Canvas only allows http links, but here we just submit anyway and let canvas do error checking.
    # Confirm
    conf = inquirer.confirm(
        message="Are you sure you want to submit"
    ).execute()
    if not conf:
        return
    # Submit!
    # TODO: Add