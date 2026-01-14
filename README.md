Gmail to Google Sheets Automation
Name: Sanjeet Kumar
---> Project Overview
This project is a Python-based automation system that reads unread emails from Gmail and logs
them into a Google Sheet.
It ensures no duplicate entries, uses OAuth 2.0 authentication, and marks emails as read after
processing.
---> Objective
To demonstrate Gmail API and Google Sheets API integration using Python with proper state
handling and duplicate prevention.
--->High-Level Architecture
Gmail Inbox → Gmail API → Python Script → Google Sheets API → Google Sheet
--->Project Structure
GMAILTOSHEET/
 src/
 credentials/
 config.py
 requirements.txt
 state.json
 .gitignore
 README.md
--->OAuth Flow
OAuth 2.0 Installed App Flow is used. Tokens are stored locally and refreshed automatically.
--->Duplicate Prevention
Processed Gmail message IDs are stored in state.json to avoid reprocessing emails.
--->State Persistence
State is stored in a local JSON file using unique Gmail message IDs.
--->Challenges
OAuth scope errors and Google Sheets cell-size limitations were resolved by centralized scopes
and safe truncation.
--->Limitations
Processes only unread inbox emails and stores state locally.
--->Conclusion
This project showcases secure, modular, and scalable Python automation using Gmail and Google
Sheets APIs.


How to run this project

🔹Prerequisites
Python 3.9 or above
A Gmail account
Google Cloud Project with:
Gmail API enabled
Google Sheets API enabled


🔹Step 1: Clone the Repository
git clone <your-repository-url>
cd GMAILTOSHEET


🔹Step 2: Install Required Dependencies
All required libraries are listed in requirements.txt.
        pip install -r requirements.txt



🔹Step 4: Add Google OAuth Credentials
Download credentials.json from Google Cloud Console
Place it inside:
credentials/credentials.json


🔹Step 5: Configure Google Sheet
Update config.py with your Google Sheet details:
SPREADSHEET_ID = "YOUR_SPREADSHEET_ID"
SHEET_NAME = "Emails"


🔹Step 6: Run the Application
Always run the project from the root directory using:
    python -m src.main

