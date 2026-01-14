import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from config import (
    SCOPES,
    SPREADSHEET_ID, 
    SHEET_NAME
)
# Same OAuth token will be reused
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/gmail.modify'
]


def get_sheets_service():
    """
    Google Sheets API service banata hai
    """
    creds = None

    if os.path.exists('token.json'):
        with open('token.json', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials/credentials.json',
                SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open('token.json', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)
    return service


def ensure_header_row(service):
    """
    Sheet mein header row exist karti hai ya nahi check karta hai
    """
    range_name = f"{SHEET_NAME}!A1:D1"
    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=range_name
    ).execute()

    values = result.get('values', [])

    if not values:
        headers = [["From", "Subject", "Date", "Content"]]
        service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=range_name,
            valueInputOption="USER_ENTERED",
            body={"values": headers}
        ).execute()


def append_email_row(service, email_data):
    MAX_CELL_CHARS = 4000

    content = email_data.get("body", "")
    if len(content) > MAX_CELL_CHARS:
        content = content[:MAX_CELL_CHARS] + "\n\n[TRUNCATED]"

    row = [[
        email_data.get("from", ""),
        email_data.get("subject", ""),
        email_data.get("date", ""),
        content
    ]]

    service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{SHEET_NAME}!A:D",
        valueInputOption="USER_ENTERED",
        insertDataOption="INSERT_ROWS",
        body={"values": row}
    ).execute()
