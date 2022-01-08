# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

# Import dependencies to use Google Sheets API

# To use to access and update data in spreadsheet
import gspread

# To set up authentication with creds.json to access the project on Google Cloud
from google.oauth2.service_account import Credentials

# Used from CI Love Sandwiches walkthrough project to access data on the spreadsheet
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('winter_wedding')

main = SHEET.worksheet('main')

values = main.get_all_values()
print(values)