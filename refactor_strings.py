import datetime
import re

def refactor_strings(exam_string):
    """
    Extracts and formats date, title, and description from an exam string.

    Args:
        exam_string (str): The string containing exam details.

    Returns:
        tuple: A tuple containing the date (str), title (str), and description (str).

    Raises:
        ValueError: If the values cannot be extracted from the exam string.
    """
    date_pattern = r"deadline=DateTime\(timestamp=\d+, date=datetime\.date\((\d+), (\d+), (\d+)\)"
    title_pattern = r"name='([^']+)'(?!.*name='[^']+')"  # Match the last occurrence for the subject
    description_pattern = r"topic='([^']+)'"

    date_match = re.search(date_pattern, exam_string)
    title_match = re.search(title_pattern, exam_string)
    description_match = re.search(description_pattern, exam_string)

    if not (date_match and title_match and description_match):
        raise ValueError("Could not extract values from the exam string.")

    year, month, day = map(int, date_match.groups())
    date = datetime.date(year, month, day).isoformat()
    title = title_match.group(1)
    description = description_match.group(1)
    return date, title, description