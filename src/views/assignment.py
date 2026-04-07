from InquirerPy import inquirer
from InquirerPy.base import Choice
from datetime import datetime
from babel.dates import format_datetime
import requests
import views.submit
import utils

def main(server: dict, course: dict, assignment: dict):
    while True:
        # Clear the screen
        utils.clear(server['name'], course['shortName'], "Assignments", assignment.get('title') or assignment.get('name'))
        # Check if the assignment is the full details, if not, fetch them.
        if 'description' not in assignment:
            # Get assignment contents
            assignmentreq = utils.get_endpoint(assignment['url'])
            assignment = assignmentreq['json']
        # Print details and set choices
        choices = []
        if assignment['points_possible']:
            print(str(assignment['points_possible']) + " points")
        if assignment['omit_from_final_grade']:
            print("This assignment does not count toward your final grade")
        if assignment['has_submitted_submissions']:
            print("You have submitted this assignment")
        else:
            print("This assignment is missing")
        if assignment['unlock_at']:
            print(f"Unlocked at {format_datetime(datetime.fromisoformat(assignment['unlock_at']))}")
        if assignment['due_at']:
            print(f"Due at {format_datetime(datetime.fromisoformat(assignment['due_at']))}")
        else:
            print("This assignment does not have a due date")
        if assignment['lock_at']:
            print(f"Locks at {format_datetime(datetime.fromisoformat(assignment['lock_at']))}")
        if assignment.get('availability_status') and assignment['availability_status']['status'] == "closed":
            print("Locked: " + assignment.get("lock_explanation", "This assignment was locked"))
        choices.append(Choice("submission", "View submission"))
        choices.append(Choice("back", "Back"))
        # Show description
        if assignment['description']: # Sometimes the description is blank
            print("\nDescription:")
            utils.printHTML(assignment['description'])
        print("\n")
        # Ask for input
        item = inquirer.select(
            message="Select an option",
            choices=choices,
            qmark="",
            amark=">",
            show_cursor=False
        ).execute()
        match item:
            case "back":
                break
            case "submission":
                view_submission(server, course, assignment)

def view_submission(server: dict, course: dict, assignment: dict):
    while True:
        # Clear the screen
        utils.clear(server['name'], course['shortName'], "Assignments", assignment['name'], "Submission")
        # Get the submission
        subreq = utils.get_endpoint(f"/api/v1/courses/{course['id']}/assignments/{assignment['id']}/submissions/self?include[]=submission_comments")
        submission = subreq['json']
        if submission['score']:
            if assignment['points_possible']:
                print(f"You got {submission['score']}/{assignment['points_possible']} points")
            else:
                print(f"You got {submission['score']} points")
        if submission['submitted_at']:
            print(f"Submitted at {format_datetime(datetime.fromisoformat(submission['submitted_at']))}")
        if not submission['grade_matches_current_submission']:
            print("Your current grade does not match your current submission")
        if submission['submission_type']:
            print(f"Submission type: {submission['submission_type']}")
        if submission['excused']:
            print("You were excused from this assignment")
        if submission['late']:
            print("This assignment is late!")
        if submission['missing']:
            print("This assignment is missing!")
        choices = [
            Choice("comments", f"View comments ({len(submission['submission_comments'])})")
        ]
        if "online_text_entry" in assignment['submission_types'] or "online_url" in assignment['submission_types'] or "online_upload" in assignment['submission_types']:
            choices.append(Choice("submit", "Submit assignment"))
        choices.append(Choice("back", "Back"))
        # Ask for input
        item = inquirer.select(
            message="Select an option",
            choices=choices,
            qmark="",
            amark=">",
            show_cursor=False
        ).execute()
        match item:
            case "back":
                break
            case "comments":
                view_subcomments(server, course, assignment, submission)
            case "submit":
                views.submit.main(server, course, assignment)

def view_subcomments(server: dict, course: dict, assignment: dict, submission: dict):
    while True:
        comments = submission['submission_comments']
        # Clear the screen
        utils.clear(server['name'], course['shortName'], "Assignments", assignment['name'], "Submission", "Comments")
        cattempt = None
        for comment in comments:
            if comment['attempt'] != cattempt:
                print(f"- Attempt {comment['attempt']} -\n")
                cattempt = comment['attempt']
            print(f"{comment['author_name']}:\n{comment['comment']}\n")
        item = inquirer.select(
            message="Select an option",
            choices=[
                Choice("comment", "Add comment"),
                Choice("back", "Back")
            ],
            qmark="",
            amark=">",
            show_cursor=False
        ).execute()
        match item:
            case "back":
                break
            case "comment":
                add_subcomment(server, course, assignment, submission)
        
def add_subcomment(server: dict, course: dict, assignment: dict, submission: dict):
    # Request comment
    cmt = inquirer.text(
        message="Enter comment text:",
        multiline=True,
    ).execute()
    # Confirm
    conf = inquirer.confirm(
        message="Are you sure you want to add this comment"
    ).execute()
    if not conf:
        return
    # Add it!
    t = requests.put(f"{server['url']}/api/v1/courses/{course['id']}/assignments/{assignment['id']}/submissions/self", params={"comment[text_comment]": cmt, "comment[attempt]": submission['attempt']}, headers={"Authorization": f"Bearer {server['token']}"}, timeout=10)
    submission['submission_comments'] = t.json()['submission_comments']
    utils.clear_request_cache()