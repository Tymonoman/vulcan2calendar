import datetime
import re


def refactor_strings(exam_string):
    global date, title, description
    date_pattern = r"deadline=DateTime\(timestamp=\d+, date=datetime\.date\((\d+), (\d+), (\d+)\)"
    title_pattern = r"name='([^']+)'(?!.*name='[^']+')"  # Match the last occurrence for the subject
    description_pattern = r"topic='([^']+)'"

    # Extracting the values
    date_match = re.search(date_pattern, exam_string)
    title_match = re.search(title_pattern, exam_string)
    description_match = re.search(description_pattern, exam_string)

    if date_match and title_match and description_match:
        # Create a formatted date string
        year = int(date_match.group(1))
        month = int(date_match.group(2))
        day = int(date_match.group(3))
        date_obj = datetime.date(year, month, day)

        # Store the formatted date for the Google Calendar API
        date = date_obj.isoformat()  # ISO format for Google Calendar
        title = title_match.group(1)
        description = description_match.group(1)

        print(f"Date: {date}")
        print(f"Title: {title}")
        print(f"Description: {description}")
    else:
        print("Could not extract values.")

    return date, title, description
