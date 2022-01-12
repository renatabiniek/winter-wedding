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
You've been invited to our winter wedding!\n
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
        print("Checking your email address...")

        if validate_email(email_str):
            print("Email is valid\n")
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
    print("Adding responses to main worksheet...\n")
    main_worksheet = SHEET.worksheet("main")

    # first_empty_row = (len(main_worksheet.get_all_values()) + 1)
    # main_worksheet.update_cell(first_empty_row, 2, email)
    # get_timestamp()
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
    rsvp_info.append(stamp)
    return stamp


def get_y_n():
    """
    Gets Yes or No response from the guest.
    Y if attending, N if not attending.
    """
    while True:
        print("We really hope to see you there!")
        print("Are you able to join us?")
        yes_or_no = input("Enter Y (Yes) or N (No):\n").upper()

        if validate_y_n(yes_or_no):
            rsvp_info.append(yes_or_no)
            print("Checking your response...\n")
            break

    accept_or_decl(yes_or_no)
    return yes_or_no


def validate_y_n(value):
    """
    Checks that the response is Y or N,
    returns True if valid response.
    """
    responses = ["Y", "N"]
    try:
        if value not in responses:
            raise ValueError(
                f"You responded {value}. This seems incorrect"
            )
    except ValueError as e:
        print(f"Invalid value: {e}, please enter Y or N.\n")
        return False

    return True


def accept_or_decl(value):
    """
    Checks for accept or decline response.
    If response is No, this ends the program.
    If it's Yes, next question is displayed.
    """
    if value == "N":
        print("We're sorry you can't make it.")
        print("Thank for letting us know.")
        print("We'll save you some cake!")

    elif value == "Y":
        print("You said YES!")
        print("We're looking forward to seeing you on the day.\n")
        no_of_guests()
        get_diet()


# Based on the Love Sandwiches project and adjusted
def no_of_guests():
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

    return guest


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
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True


def validate_adult_att(values):
    """
    Checks that there is at least one adult attending,
    and no more than two adults per invite,
    by validating that the first integer in the list
    is not == 0 and not > 2. Also check that there is
    no more than 4 kids per invitee.
    """
    print("Validating number of guests...")
    guests_int = [int(value) for value in values]
    adults = guests_int[0]
    kids = guests_int[1]

    try:
        [int(value) for value in values]
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
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

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
            print("Meal choice is valid")
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
    meals = ["V", "VG", "GF", "S"]

    try:
        if value not in meals:
            raise ValueError(
                f"Options are: V, VG, GF or S. You entered {value}"
                )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True

# def add_timestamp(date):
#     """
#     Identify first empty row on main worksheet and add guest email
#     """
#     print("Adding date of submission to main worksheet...\n")
#     main_worksheet = SHEET.worksheet("main")
#     first_empty_row = (len(main_worksheet.get_all_values()) + 1)
#     main_worksheet.update_cell(first_empty_row, 1, date)
#     print("Timestamp added to main worksheet...!")


def main():
    """
    Runs all program functions.
    """
    submission_date = get_timestamp()
    # add_timestamp(submission_date)
    guest_email = get_guest_info()
    rsvp_response = get_y_n()
    add_guest(rsvp_info)
    print(rsvp_info)


main()