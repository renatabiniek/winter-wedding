# Import re module to validate email address
import re

# To get current time and date
from datetime import datetime

# Import dependencies to use Google Sheets API
# To use to access and update data in spreadsheet
import gspread

# To set up authentication with creds.json
# and access the project on Google Cloud
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
You've been invited to our winter wedding!
Please RSVP here.
    ''')


print_logo()

# Empty list to collect responses from terminal and
# later append to the main worksheet
rsvp_info = []


def get_guest_info():
    """
    Get email address from the guest
    """
    email_str = None
    while True:
        print("What's your email address?")
        email_str = input("Enter email address:\n").lower()
        print("Checking your email address...")

        if validate_email(email_str):
            print("Email is valid\n")
            # rsvp_info.append(email_str)
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
    regex = re.compile(
        r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]'
        r'+(\.[A-Z|a-z]{2,})+')

    try:
        if not re.fullmatch(regex, email):
            raise ValueError(
                f"Email {email} seems incorrect"
            )
    except ValueError as error:
        print(f"Invalid data: {error}, please enter your email again.\n")
        return False

    return True


def add_guest(data):
    """
    Append new row with collected
    responses.
    """
    print("Adding responses to main worksheet...\n")
    main_worksheet = SHEET.worksheet("main")

    # first_empty_row = (len(main_worksheet.get_all_values()) + 1)
    # main_worksheet.update_cell(first_empty_row, 2, email)
    main_worksheet.append_row(data)

    print("Responses added to main worksheet...!")


def get_timestamp():
    """
    Gets current date and time and parses it into the selected format
    and appends to the rsvp_info list
    """
    now = datetime.now()
    # Format the date and time as dd/mm/YY H:M:S
    stamp = now.strftime("%d/%m/%Y %H:%M:%S")

    return stamp


def get_response():
    """
    Gets Yes or No response from the guest.
    Y if attending, N if not attending.
    """
    while True:
        print("We really hope to see you there!")
        print("Are you able to join us?")
        guest_response = input("Enter Y (Yes) or N (No):\n").upper()

        if validate_response(guest_response):
            rsvp_info.append(guest_response)
            print("Checking your response...\n")
            break

    handle_accept_or_decl(guest_response)
    return guest_response


def validate_response(value):
    """
    Checks that the response is Y or N,
    returns True if valid response.
    """
    if value not in ["Y", "N"]:
        return False

    return True


def handle_accept_or_decl(value):
    """
    Checks for accept or decline response.
    If response is No, this ends the program.
    If it's Yes, next question is displayed.
    """
    if value == "N":
        print("We're sorry you can't make it.")
        print("But don't worry,")
        print("we'll save you some cake!")

    elif value == "Y":
        print("You said YES!")
        print("We're looking forward to seeing you on the day.\n")
        get_number_of_guests()
        get_diet()


def get_number_of_guests():
    """
    Request number of adult guests and no of children
    as a list of strings separated by commas.
    """
    while True:
        print("Let us know who's coming with you.")
        print("One invitation is for max. 2 adults and 6 kids.")
        print("Enter two numbers, first adults, then kids,")
        print("separated by commas.")
        print("Example: 2, 1\n")

        guests_str = input("Enter number of adults and kids here:\n")
        guests = guests_str.split(",")

        if validate_no_of_guests(guests) and validate_adult_att(guests):
            for guest in guests:
                rsvp_info.append(guest)
            print("Number of guests is correct.\n")
            break

    return guests


def validate_no_of_guests(values):
    """
    Converts strings with numbers to integers,
    raises ValueError if string cannot be converted into a number,
    if there aren't exactly 2 values.
    """
    try:
        [int(value) for value in values]
        if len(values) != 2:
            raise ValueError(
                f"Two numbers are required, you provided {len(values)}"
            )
    except ValueError as error:
        print(f"Invalid data: {error}, please try again.\n")
        return False

    return True

    # numb_of_guests = [int(value) for value in values]

    # if len(numb_of_guests) != 2:
    #     print(f"Two numbers are required,
    #     you provided {len(numb_of_guests)}.")
    #     print("Please try again.\n")
    #     return False

    # return True


def validate_adult_att(values):
    """
    Checks that there is at least one adult attending,
    and no more than two adults per invite,
    by validating that the first integer in the list
    is not == 0 and not > 2. Also check that there is
    no more than 6 kids per invitee.
    """
    print("Validating number of guests...")

    try:
        guests_int = [int(value) for value in values]
        adults = guests_int[0]
        kids = guests_int[1]
        if adults == 0:
            raise ValueError(
                f"Looks like {adults} adults are attending"
            )
        elif adults > 2:
            raise ValueError(
                f"Only 2 adults per invite, you entered {adults}"
            )
        elif kids > 6:
            raise ValueError(
                f"Only upto 6 kids are allowed, you entered {kids}"
            )
    except ValueError as error:
        print(f"Invalid data: {error}, please try again.\n")
        return False

    # guests_int = [int(value) for value in values]
    # adults = guests_int[0]
    # kids = guests_int[1]
    # if adults == 0:
    #     print("Something went wrong.")
    #     print(f"Looks like {adults} adults are attending.")
    #     print("Please try again.\n")
    #     return False
    # elif adults > 2:
    #     print("Something went wrong.")
    #     print(f"Only 2 adults per invite, you entered {adults}.")
    #     print("Please try again.\n")
    #     return False
    # elif kids > 6:
    #     print("Something went wrong.")
    #     print(f"Only upto 6 kids are allowed, you entered {kids}.")
    #     print("Please try again.\n")
    #     return False
    return True


def get_diet():
    """
    Requests the guest to select dietary requirements.
    Repeat request until valid meal option selected.
    If valid, append the choice to the rsvp_info.
    """

    while True:
        print("Please let us know what meal you'd prefer.")
        print("V (vegetarian), VG (vegan), GF (glutenfree), S (standard).")
        meal_data = input("Enter your choice here: \n")
        meal_choice_up = meal_data.upper()
        if validate_meal_choice(meal_choice_up):
            rsvp_info.append(meal_choice_up)
            break

    print(f"You selected {meal_choice_up}")

    return meal_choice_up


def validate_meal_choice(value):
    """
    Checks that the value entered by the user
    matches the available options.
    """
    print("Validating meal choice...")

    if value not in ["V", "VG", "GF", "S"]:
        print(f"Options are: V, VG, GF or S. You entered {value}")
        print("Please try again.\n")
        return False

    return True


def is_returning_guest(email):
    """Checks if email already exists
    in the email column on the main spreadsheet and
    prints a message to the guest to RSVP had already been recorded"""

    guest_list = SHEET.worksheet("main").col_values(2)

    if email in guest_list:
        print("Welcome back! We already have your RSVP.")
        return True


def find_a_row(value):
    """
    Finds a row with matching email string
    and return row number
    """
    row_with_guest = SHEET.worksheet("main").find(value)
    print(row_with_guest.row)

    return row_with_guest.row


def return_response_details(value):
    """
    Reads values in header row and
    values in the row with the specific email address
    and creates a dictionary from those 2 lists
    """
    header_row = SHEET.worksheet("main").row_values(1)
    print(header_row)
    rsvp_row = SHEET.worksheet("main").row_values(value)
    print(rsvp_row)

    # code from
    # https://thispointer.com/python-how-to-convert-a-list-to-dictionary/
    # adjusted to suit my needs

    zip_rsvp = zip(header_row, rsvp_row)
    rsvp_dictionary = dict(zip_rsvp)

    return rsvp_dictionary


def print_rsvp_details(dictionary):
    """
    Print details of the rsvp dictionary
    in a more readable format back to the guest
    """

    for response in dictionary:
        print(response + ": " + dictionary[response])


def end_program():
    """
    Prints end message and exits the program
    """
    print("--------------------------------")
    print("THANK YOU FOR USING THIS PROGRAM\n")
    print("Click Run Program to run it again.")


def confirm_rsvp():
    """
    Prints message to guest to confirm
    RSVP has been recorded and prints summary
    of their responses in terminal.
    """
    print("Thank you for letting us know!")
    print("We recorded your RSVP as follows:")


def main():
    """
    Runs all program functions.
    """
    guest_email = get_guest_info()

    if is_returning_guest(guest_email):
        rsvp_row_number = find_a_row(guest_email)
        rsvp_summary = return_response_details(rsvp_row_number)
        print_rsvp_details(rsvp_summary)
        end_program()
    else:
        submission_date = get_timestamp()
        rsvp_info.append(submission_date)
        rsvp_info.append(guest_email)
        rsvp_response = get_response()
        add_guest(rsvp_info)
        confirm_rsvp()
        rsvp_row_number = find_a_row(guest_email)
        rsvp_summary = return_response_details(rsvp_row_number)
        print_rsvp_details(rsvp_summary)
        end_program()


main()
