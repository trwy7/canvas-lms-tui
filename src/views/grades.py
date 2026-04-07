from InquirerPy import inquirer
from InquirerPy.base import Choice
import utils

def main(server: dict, course: dict):
    #while True:
    # Clear the screen
    utils.clear(server['name'], course['shortName'], "Grades")
    # Get score
    course_req = utils.get_endpoint(f"/api/v1/courses/{course['id']}?include[]=total_scores")
    gcourse = course_req['json']
    # Check if there is a score available
    if gcourse['enrollments'][0]['computed_current_score']:
        # Check if a letter grade is available
        if gcourse['enrollments'][0]['computed_current_grade']:
            print(f"Current grade: {str(gcourse['enrollments'][0]['computed_current_score'])}% ({str(gcourse['enrollments'][0]['computed_current_grade'])})")
            print(f"Current grade (including ungraded): {str(gcourse['enrollments'][0]['computed_final_score'])}% ({str(gcourse['enrollments'][0]['computed_final_grade'])})")
        else:
            print(f"Current grade: {str(gcourse['enrollments'][0]['computed_current_score'])}")
            print(f"Current grade (including ungraded): {str(gcourse['enrollments'][0]['computed_final_score'])}")
    else:
        print("Was not able to get current grade")
    input("\nPress enter to exit...")
        #break
        # TODO: /api/v1/courses/<id>/students/submissions for individual assignments, then uncomment the while true
        # The response formatting of the above looks like it will break on teacher accounts
        # While we don't target teachers, I want the app to be as compatible as possible with both.