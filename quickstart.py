from __future__ import print_function

import datetime
import os.path
import requests
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
        print("Getting the upcoming 10 events")
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            print("No upcoming events found.")
            return

        clicktime_payload = None

        # Prints the start and name of the next 10 events
        for event in events:
            import pdb

            pdb.set_trace()
            start_hour = event["start"].get("dateTime")[:-6]
            start_hour = datetime.datetime.strftime(start_hour, "%y-%m-%dT%H:%M:%S")
            end_hour = event["start"].get("dateTime")[:-6]
            end_hour = datetime.datetime.strftime(start_hour, "%y-%m-%dT%H:%M:%S")
            hours = (start_hour - end_hour).hour

            if "1:1 distillery" in event["summary"].lower():
                clicktime_payload = {
                    "BreakTime": None,
                    "Comment": "",
                    "Date": "2022-06-13",
                    "EndTime": None,
                    "Hours": hours,
                    "ID": "EDITED",
                    "JobID": "EDITED",
                    "StartTime": None,
                    "TaskID": "EDITED",
                    "UserID": "EDITED",
                }

            elif "daily" in event["summary"].lower():
                clicktime_payload = {
                    "BreakTime": None,
                    "Comment": "",
                    "Date": "2022-06-13",
                    "EndTime": None,
                    "Hours": hours,
                    "ID": "EDITED",
                    "JobID": "EDITED",
                    "StartTime": None,
                    "TaskID": "EDITED",
                    "UserID": "EDITED",
                }

            start = event["start"].get("dateTime", event["start"].get("date"))
            print(start, event["summary"])

            # ClickTime Request
            url = "EDITED"
            headers = {
                "Authorization": "EDITED",
                "Content-Type": "application/json",
            }
            response = requests.request(
                "POST", url, headers=headers, data=clicktime_payload
            )

    except HttpError as error:
        print("An error occurred: %s" % error)


if __name__ == "__main__":
    main()
