# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

# Import dependencies to use Google Sheets API

# To use to access and update data in spreadsheet
import gspread

# To set up authentication with creds.json to access the project on Google Cloud
from google.oauth2.service_account import Credentials

# Import re module to validate email address

import re

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

def get_guest_info():
    """
    Get email address from the guest
    """
    print("What's your email address?\n")

    email_str = input("Enter email address:\n")
    print("Checking your email address...\n")
    validate_email(email_str)


# From https://stackabuse.com/python-validate-email-address-with-regular-expressions-regex/

def validate_email(email):
    """
    Using Regular Expression, validates basic syntax of email address
    """
    # Regular expression for validating the email
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

    try:
        if (not re.fullmatch(regex, email)):
            raise ValueError(
                f"Email {email} seems incorrect"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please enter your email address again.\n")

get_guest_info()