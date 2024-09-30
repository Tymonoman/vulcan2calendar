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

SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate():
    """
    Authenticates the user and returns a Google Calendar API service instance.

    Returns:
        googleapiclient.discovery.Resource: The authenticated Google Calendar API service instance.
    """
    creds = None
    token_path = '.venv/token.pickle'

    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    return build('calendar', 'v3', credentials=creds)

def create_event(service):
    """
    Creates events in Google Calendar for each exam.

    Args:
        service (googleapiclient.discovery.Resource): The authenticated Google Calendar API service instance.
    """
    exam_list = asyncio.run(get_exams())
    for exam in exam_list:
        try:
            date, title, description = refactor_strings(str(exam))
            if not event_exists(service, date, title):
                event = create_calendar_event(date, title, description)
                event = service.events().insert(calendarId='primary', body=event).execute()
                print(f'Event created: {event.get("htmlLink")}')
            else:
                print(f"Event '{title}' already exists on {date}. Skipping creation.")
        except ValueError as e:
            print(f"Error processing exam: {e}")

def event_exists(service, date, title):
    """
    Checks if an event with the same title already exists on the given date.

    Args:
        service (googleapiclient.discovery.Resource): The authenticated Google Calendar API service instance.
        date (str): The date of the event in ISO format.
        title (str): The title of the event.

    Returns:
        bool: True if an event with the same title exists on the given date, False otherwise.
    """
    events = service.events().list(
        calendarId='primary',
        timeMin=f"{date}T00:00:00Z",
        timeMax=f"{date}T23:59:59Z",
        q=title,
        singleEvents=True,
        orderBy='startTime'
    ).execute().get('items', [])
    return any(event['summary'] == title for event in events)

def create_calendar_event(date, title, description):
    """
    Creates a dictionary representing a calendar event.

    Args:
        date (str): The date of the event in ISO format.
        title (str): The title of the event.
        description (str): The description of the event.

    Returns:
        dict: A dictionary representing the calendar event.
    """
    return {
        'summary': title,
        'description': description,
        'start': {'date': date, 'timeZone': 'Europe/Warsaw'},
        'end': {'date': (datetime.date.fromisoformat(date) + datetime.timedelta(days=1)).isoformat(), 'timeZone': 'Europe/Warsaw'},
    }

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    service = authenticate()
    create_event(service)