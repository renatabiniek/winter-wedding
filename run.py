# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

# Import re module to validate email address

import re

# To get current time and date
from datetime import datetime
# Import dependencies to use Google Sheets API

# To use to access and update data in spreadsheet
import gspread

# To set up authentication with creds.json 
# to access the project on Google Cloud
from google.oauth2.service_account import Credentials


# Used from CI Love Sandwiches walkthrough project 
# to access data on the spreadsheet
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('winter_wedding')

def print_logo():
    """
    Prints an intro image.
    From asciiart.
    """

    print('''
         (\/)
          \/
  (\/)   .-.  .-.
   \/   ((`-)(-`))
         \\    //   (\/)
          \\  //     \/
   .="""=._))((_.="""=.
  /  .,   .'  '.   ,.  \\
 /__(,_.-'      '-._,)__\\
`    /|             |\   `
    /_|__         __|_\\
      | `))     ((` |
      |             |
     -"==         =="-
    \n 
You've been invited to our wedding!\n
Please RSVP here.\n
    ''')


print_logo()

# Empty list to collect responses from terminal and
# later append to the main worksheet 
rsvp_info = []

def get_guest_info():
    """
    Get email address from the guest
    """
    while True:
        print("What's your email address?\n")
        email_str = input("Enter email address:\n").lower()
        print("Checking your email address...\n")
        
        if validate_email(email_str):
            print("Email is valid")
            rsvp_info.append(email_str)
            break

    return email_str


# From https://stackabuse.com/

def validate_email(email):
    """
    Using Regular Expression, validates basic syntax of email address.
    Inside the try element, raises ValueErrors if the email
    doesn't match the expected syntax.
    Returns True if email is valid.
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
        return False 
    
    return True


def add_guest(data):
    """
    Identify first empty row on main worksheet and add guest email
    """
    print("Adding guest email and timestamp to main worksheet...\n")
    main_worksheet = SHEET.worksheet("main")

    # first_empty_row = (len(main_worksheet.get_all_values()) + 1)
    # main_worksheet.update_cell(first_empty_row, 2, email)
    # get_timestamp()    
    main_worksheet.append_row(data)

    print("Email and stamp added to main worksheet...!")

def get_timestamp():
    """
    Gets current date and time and parses it into the selected format
    and appends to the rsvp_info list
    """
    now = datetime.now()
    # Format the date and time as dd/mm/YY H:M:S
    stamp = now.strftime("%d/%m/%Y %H:%M:%S")
    rsvp_info.append(stamp)
    return stamp

def get_y_n():
    """
    Gets Yes or No response from the guest.
    Y if attending, N if not attending.
    """
    print("We really hope to see you there!")
    y_or_no = input("Are you able to join us? Enter Y (Yes) or N (No)\n").upper()
    print("Recording your response...\n")
    print(y_or_no)
    


# def add_timestamp(date):
#     """
#     Identify first empty row on main worksheet and add guest email
#     """
#     print("Adding date of submission to main worksheet...\n")
#     main_worksheet = SHEET.worksheet("main")
#     first_empty_row = (len(main_worksheet.get_all_values()) + 1)
#     main_worksheet.update_cell(first_empty_row, 1, date)
#     print("Timestamp added to main worksheet...!")


submission_date = get_timestamp()
# add_timestamp(submission_date)
guest_email = get_guest_info()
add_guest(rsvp_info)
get_y_n()
print(rsvp_info)