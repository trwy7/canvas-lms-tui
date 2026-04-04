from InquirerPy import inquirer
from InquirerPy.base import Choice
from datetime import datetime
from babel.dates import format_datetime
import utils

def main(server: dict, course: dict, assignment: dict):
    while True:
        # Clear the screen
        utils.clear(server['name'], course['shortName'], "Assignments", assignment['title'])
        # Get assignment contents
        assignmentreq = utils.get_endpoint(assignment['url'])
        jassignment = assignmentreq['json']
        # Print details and set choices
        choices = []
        if jassignment['points_possible']:
            print(str(jassignment['points_possible']) + " points")
        if jassignment['omit_from_final_grade']:
            print("This assignment does not count toward your final grade")
        if jassignment['has_submitted_submissions']:
            print("You have submitted this assignment")
        else:
            print("This assignment is missing")
        if jassignment['unlock_at']:
            print(f"Unlocked at {format_datetime(datetime.fromisoformat(jassignment['unlock_at']))}")
        if jassignment['due_at']:
            print(f"Due at {format_datetime(datetime.fromisoformat(jassignment['due_at']))}")
        else:
            print("This assignment does not have a due date")
        if jassignment['lock_at']:
            print(f"Locks at {format_datetime(datetime.fromisoformat(jassignment['lock_at']))}")
        if jassignment.get('availability_status') and jassignment['availability_status']['status'] == "closed":
            print("Locked: " + jassignment.get("lock_explanation", "This assignment was locked"))
        choices.append(Choice("submission", "View submission"))
        choices.append(Choice("back", "Back"))
        # Show description
        if jassignment['description']: # Sometimes the description is blank
            print("\nDescription:")
            utils.printHTML(jassignment['description'])
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
                view_submission(server, course, jassignment)

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
            message="Select an item",
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
                raise NotImplementedError()

def view_subcomments(server: dict, course: dict, assignment: dict, submission: dict):
    input(submission['submission_comments'])