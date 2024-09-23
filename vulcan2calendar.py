import asyncio
import datetime
import os
import pickle
import sys

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from get_exams import get_exams
from refactor_strings import refactor_strings

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def authenticate():
    """Shows basic usage of the Google Calendar API.
    Creates a Google Calendar API service instance.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('.venv/token.pickle'):
        with open('.venv/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('.venv/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('calendar', 'v3', credentials=creds)


def create_event(service):
    exam_list = asyncio.run(get_exams())
    for exam in exam_list:
        exam_string = str(exam)  # Convert exam to string
        date, title, description = refactor_strings(exam_string)

        # Check for existing events on the same date
        existing_events = service.events().list(
            calendarId='primary',
            timeMin=f"{date}T00:00:00Z",  # Start of the day
            timeMax=f"{date}T23:59:59Z",  # End of the day
            q=title,  # Query for events with the same title
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        # Check if any existing event matches the title
        events = existing_events.get('items', [])
        if any(event['summary'] == title for event in events):
            print(f"Event '{title}' already exists on {date}. Skipping creation.")
            continue  # Skip creating this event

        # Create the new event
        event = {
            'summary': title,
            'description': description,
            'start': {
                'date': date,  # All-day events use the 'date' field
                'timeZone': 'Europe/Warsaw',
            },
            'end': {
                'date': (datetime.date.fromisoformat(date) + datetime.timedelta(days=1)).isoformat(),
                'timeZone': 'Europe/Warsaw',
            },
        }

        event = service.events().insert(calendarId='primary', body=event).execute()
        print(f'Event created: {event.get("htmlLink")}')


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    service = authenticate()
    create_event(service)
