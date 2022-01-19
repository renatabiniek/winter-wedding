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

# Validation set for options available
# at the start (wedding guest or coordinator)
GUEST_COORDINATOR_VALIDATION_SET = ['W', 'C']


def show_intro_options():
    """
    Prints 2 options to the user:
    to RSVP or to access admin overview.
    Request for input is repeated until input valid.
    """
    print("--------------------------------------")
    print("Welcome to the RSVP Tool!")
    print("--------------------------------------\n")
    print("If you got our wedding invite, select W.")
    print("If you're the event coordinator, select C.\n")
    option_str = None
    while True:
        option_str = input("Enter W or C:\n").upper()
        print("Checking your input...")

        if validate_input(option_str, GUEST_COORDINATOR_VALIDATION_SET):
            print("Input is valid!\n")
            break

    return option_str


def validate_input(value, validation_set=['Y', 'N']):
    """
    Validates option selected is contained
    in validation set and returns the option
    """
    return value in validation_set


def run_selected_option(value):
    """
    Runs next functions for each selected option.
    """
    if value == "W":
        print("Accessing the RSVP tool...")
        print_logo()
        guest_email = get_guest_info()

        # If email already on the worksheet, confirm
        # RSVP recorded and end program
        if is_returning_guest(guest_email):
            rsvp_row_number = find_a_row(guest_email)
            rsvp_summary = return_response_details(rsvp_row_number)
            print_rsvp_details(rsvp_summary)
            end_program()
        else:
            submission_date = get_timestamp()

            # Empty list to hold rsvp responses
            rsvp_info = []

            # Appending responses
            rsvp_info.append(submission_date)
            rsvp_info.append(guest_email)
            rsvp_response = get_response()
            rsvp_info.append(rsvp_response)

            guests_and_meals = handle_accept_or_decl(rsvp_response)
            if guests_and_meals:
                for items in guests_and_meals:
                    rsvp_info.append(items)

            # Appends new row of responses to "main" worksheet
            add_guest(rsvp_info)
            # Calculates totals and percentage
            rsvp_total = increment_rsvp_count()
            increment_accept_or_decl(rsvp_response)
            calculate_percentage(rsvp_total)
            # Confirm RSVP, get and print RSVP details
            confirm_rsvp()
            rsvp_row_number = find_a_row(guest_email)
            rsvp_summary = return_response_details(rsvp_row_number)
            print_rsvp_details(rsvp_summary)
            # End message
            end_program()

    elif value == "C":
        print("One moment, retrieving RSVP data...\n")
        # Get and print overview of all responses
        admin_summary = get_admin_overview()
        print_rsvp_details(admin_summary)
        end_program()


def print_logo():
    """
    Prints an intro image from asciiart.
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


def get_guest_info():
    """
    Get email address from the guest.
    Repeat request until email is in valid format.
    """
    email_str = None
    while True:
        print("What's your email address?")
        email_str = input("Enter email address:\n").lower()
        print("Checking your email address...")

        if validate_email(email_str):
            print("Email is valid!\n")
            break

    return email_str


def validate_email(email):
    """
    Using Regular Expression, validates basic syntax of email address.
    Inside the try element, raises ValueErrors if the email
    doesn't match the expected syntax.
    Returns True if email is valid.
    """
    # Regular expression for validating the email
    # From https://stackabuse.com/
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
    Append new row with collected responses
    to the main worksheet.
    """
    print("We're recording your response.")
    main_worksheet = SHEET.worksheet("main")
    main_worksheet.append_row(data)


def get_timestamp():
    """
    Gets current date and time and parses it into the selected format
    """
    now = datetime.now()
    # Format the date and time as dd/mm/YY H:M:S
    return now.strftime("%d/%m/%Y %H:%M:%S")


def get_response():
    """
    Gets Yes or No response from the guest
    invited to the wedding.
    """
    while True:
        print("We really hope to see you there!")
        print("Are you able to join us?")
        guest_response = input("Enter Y (Yes) or N (No):\n").upper()

        if validate_input(guest_response):
            print("Checking your response...\n")
            break

    return guest_response


def handle_accept_or_decl(value):
    """
    Checks for accept or decline response.
    If the response is Yes, collects data on no of guests,
    meal options and appends to result list.
    Returns result to be later appended
    to the rsvp_info list.
    """
    if value == "Y":
        print("You said YES!")
        print("We're looking forward to seeing you on the day.\n")
        guests = get_number_of_guests()
        result = []
        for guest in guests:
            result.append(guest)
        meal_selected = get_diet()
        increment_meal_choice(meal_selected)
        result.append(meal_selected)

        return result

    print("We're sorry you can't make it.")
    print("But don't worry... ")
    print("we'll save you some cake!\n")
    return None


def get_number_of_guests():
    """
    Request number of adult guests and no of children
    as a list of strings separated by a comma.
    """
    while True:
        print("Let us know who's coming with you.")
        print("One invitation is for max. 2 adults and 6 kids.")
        print("Enter two numbers, first adults, then kids,")
        print("separated by commas.")
        print("Example: 2, 1\n")

        guests_str = input("Enter number of adults and kids here:\n")
        guests = guests_str.split(",")

        if validate_attendances(guests):
            print("Number of guests is correct!\n")
            break

    return guests


def validate_attendances(values):
    """
    Inside try, converts strings with numbers to integers.
    Raises ValueError if string cannot be converted into a number,
    if there aren't exactly 2 values and if unexpected number
    is entered for both - adults and kids.
    """
    try:
        int_values = [int(value) for value in values]
        if len(int_values) != 2:
            raise ValueError(
                f"Two numbers are required, you provided {len(int_values)}"
            )
        adults = int_values[0]
        kids = int_values[1]
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

    return True


def get_diet():
    """
    Requests the guest to select dietary requirements.
    Repeat request until valid meal option selected.
    If valid, return the meal choice.
    """

    while True:
        print("Please let us know what meal you'd prefer.")
        print("V (vegetarian), VG (vegan), GF (glutenfree), S (standard).\n")
        meal_data = input("Enter your choice here: \n")
        meal_choice_up = meal_data.upper()
        if validate_meal_choice(meal_choice_up):
            break

    print("Thank you, one moment please...")

    return meal_choice_up


def validate_meal_choice(value):
    """
    Checks that the value entered by the user
    matches the available options.
    """

    if value not in ["V", "VG", "GF", "S"]:
        print(f"Options are: V, VG, GF or S. You entered {value}")
        print("Please try again.\n")
        return False

    return True


def is_returning_guest(email):
    """
    Checks if email already exists
    in the email column on the main spreadsheet and
    prints a message to the guest if RSVP had already been recorded.
    """

    guest_list = SHEET.worksheet("main").col_values(2)

    if email not in guest_list:
        return False
    print("Welcome back! We already have your RSVP.")
    print("Your RSVP said:\n")

    return True


def find_a_row(value):
    """
    Finds a row with matching email string
    and returns row number with that string.
    """
    row_with_guest = SHEET.worksheet("main").find(value)
    return row_with_guest.row


def return_response_details(value):
    """
    Reads values in the header row and
    values in the row with the specific email address
    and creates a dictionary from those 2 lists
    """
    header_row = SHEET.worksheet("main").row_values(1)
    rsvp_row = SHEET.worksheet("main").row_values(value)

    # code from taken from and adjusted:
    # https://thispointer.com/python-how-to-convert-a-list-to-dictionary/

    zip_rsvp = zip(header_row, rsvp_row)
    rsvp_dictionary = dict(zip_rsvp)

    return rsvp_dictionary


def print_rsvp_details(dictionary):
    """
    Prints details of the rsvp dictionary
    in a more readable format back to the guest
    """

    for response in dictionary:
        print(response + ": " + dictionary[response])


def end_program():
    """
    Prints end message and exits the program
    """
    print("--------------------------------")
    print("THANK YOU FOR USING THIS RSVP TOOL\n")


def confirm_rsvp():
    """
    Prints message to the guest to confirm
    RSVP has been recorded and prints summary
    of their responses in terminal.
    """
    print("Thank you for letting us know!\n")
    print("We recorded your RSVP as follows:")


# Functions calculating totals start here


def increment_rsvp_count():
    """
    Converts string into integer and increments total number
    of reponses received by 1 in the RSVP column
    on totals worksheet.
    """
    print("Updating totals...")
    rsvp_total_cell = int(SHEET.worksheet("totals").acell('B2').value)
    rsvp_total_cell += 1
    update_selected_cell(2, 2, rsvp_total_cell)

    return rsvp_total_cell


def increment_accept_or_decl(value):
    """
    Increments total of Yes or No responses in
    Yes and No columns, and updates them
    on the totals worksheet.
    """
    if value == "Y":
        yes_responses_cell = int(SHEET.worksheet("totals").acell('C2').value)
        yes_responses_cell += 1
        update_selected_cell(2, 3, yes_responses_cell)
        count_adults()
        count_kids()

    elif value == "N":
        no_responses_cell = int(SHEET.worksheet("totals").acell('D2').value)
        no_responses_cell += 1
        update_selected_cell(2, 4, no_responses_cell)
    print("Finishing up...!\n")


def count_kids():
    """
    Gets all values from column Children on main worksheet
    and ignores any empty cells. Converts values to integers.
    Adds all values using sum() and inserts it in the
    specified cell on total worksheet.
    """
    # https://stackoverflow.com/questions/45134764/getting-all-column-values-from-google-sheet-using-gspread-and-python

    kids = [item for item in SHEET.worksheet("main").col_values(5) if item]
    kids_values = kids[1:]
    kids_int = [int(kid) for kid in kids_values]
    sum_kids = sum(kids_int)
    print("Calculating total number of kids")
    update_selected_cell(2, 6, sum_kids)
    return sum_kids


def count_adults():
    """
    Gets all values from column Adults on main worksheet
    and ignores any empty cells. Converts values to integers.
    Adds all values using sum() and inserts it in the
    specified cell on total worksheet.
    """
    # https://stackoverflow.com/questions/45134764/getting-all-column-values-from-google-sheet-using-gspread-and-python

    adults = [item for item in SHEET.worksheet("main").col_values(4) if item]
    adults_values = adults[1:]
    adults_int = [int(adult) for adult in adults_values]
    sum_adults = sum(adults_int)
    print("Calculating total number of adults")
    update_selected_cell(2, 5, sum_adults)
    return sum_adults


def increment_meal_choice(value):
    """
    Increments total of selected meal option
    and updates total in the relevant column on
    total worksheet.
    """

    if value == "V":
        vegetarian = int(SHEET.worksheet("totals").acell('G2').value)
        vegetarian += 1
        update_selected_cell(2, 7, vegetarian)

    elif value == "VG":
        vegan = int(SHEET.worksheet("totals").acell('H2').value)
        vegan += 1
        update_selected_cell(2, 8, vegan)

    elif value == "GF":
        gluten_free = int(SHEET.worksheet("totals").acell('I2').value)
        gluten_free += 1
        update_selected_cell(2, 9, gluten_free)

    elif value == "S":
        standard = int(SHEET.worksheet("totals").acell('J2').value)
        standard += 1
        update_selected_cell(2, 10, standard)


def calculate_percentage(value):
    """
    Calculates what percentage of responses
    has been received and rounds the result to 2 decimal places.
    """
    whole = int(SHEET.worksheet("totals").acell('A2').value)
    calc_percentage = float(value)/float(whole) * 100
    percentage = str(round(calc_percentage, 2)) + "%"
    update_selected_cell(2, 11, percentage)
    print("All done! Yor response has been recorded.\n")
    return percentage


def update_selected_cell(row, column, value):
    """
    Updates specific cell on totals worksheet
    in a specified row and column,
    with passed in value
    """
    SHEET.worksheet("totals").update_cell(row, column, value)


def get_admin_overview():
    """
    Reads values from totals worksheet
    and creates a dictionary from those 2 lists
    """
    print("Current RSVP status:\n")

    header_row = SHEET.worksheet("totals").row_values(1)
    rsvp_row = SHEET.worksheet("totals").row_values(2)

    zip_rsvp = zip(header_row, rsvp_row)
    admin_dictionary = dict(zip_rsvp)
    return admin_dictionary


def main():
    """
    Runs all program functions.
    """
    while True:
        selected_option = show_intro_options()
        run_selected_option(selected_option)
        option = ''
        while option not in ['N', 'Y']:
            option = input("Would you like to enter another " +
                           "response (y/n)? ").upper()

        if option == 'N':
            break


main()
