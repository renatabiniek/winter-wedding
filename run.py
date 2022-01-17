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


def show_intro_options():
    """
    Prints 2 options to the user:
    to RSVP or to access admin overview.
    Request for input is repeated until input valid.
    """
    print("--------------------------------------")
    print("Welcome to the RSVP Tool!")
    print("--------------------------------------\n")
    print("Are you a guest or an admin?\n")
    option_str = None
    while True:
        print("Type G to send us your RSVP or A for admin overview.")
        option_str = input("Enter G for A:\n").upper()
        print("Checking your input...")

        if validate_option(option_str):
            print("Input is valid\n")
            break

    return option_str


def validate_option(value):
    """
    Checks that the response is G or A,
    returns True if valid response.
    """
    if value not in ["G", "A"]:
        return False

    return True


def run_selected_option(value):
    """
    Runs next functions for each selected option.
    """
    if value == "G":
        print("Accessing the RSVP tool...")

    elif value == "A":
        print("One moment, retrieving RSVP data...\n")
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


# Empty list to collect responses from terminal and
# later append to the main worksheet
rsvp_info = []


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
    Append new row with collected responses.
    """
    print("Please wait, we're recording your responses...\n")
    main_worksheet = SHEET.worksheet("main")
    main_worksheet.append_row(data)


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
        print("But don't worry... ")
        print("we'll save you some cake!")

    elif value == "Y":
        print("You said YES!")
        print("We're looking forward to seeing you on the day.\n")
        get_number_of_guests()


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
            print("Number of guests is correct!\n")
            break

    return guests


def validate_no_of_guests(values):
    """
    Inside try, converts strings with numbers to integers,
    raises ValueError if string cannot be converted into a number,
    if there aren't exactly 2 values.
    """
    try:
        guest_count = [int(value) for value in values]
        if len(guest_count) != 2:
            raise ValueError(
                f"Two numbers are required, you provided {len(guest_count)}"
            )
    except ValueError as error:
        print(f"Invalid data: {error}, please try again.\n")
        return False

    return True


def validate_adult_att(values):
    """
    Checks that there is at least one adult attending,
    and no more than two adults per invite,
    by validating that the first integer in the list
    is not == 0 and not > 2. Also check that there is
    no more than 6 kids per invitee.
    """
    print("Validating number of guests...\n")

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
    If valid, append the choice to the rsvp_info list.
    """

    while True:
        print("Please let us know what meal you'd prefer.")
        print("V (vegetarian), VG (vegan), GF (glutenfree), S (standard).\n")
        meal_data = input("Enter your choice here: \n")
        meal_choice_up = meal_data.upper()
        if validate_meal_choice(meal_choice_up):
            rsvp_info.append(meal_choice_up)
            break

    # print(f"You selected {meal_choice_up}")

    return meal_choice_up


def validate_meal_choice(value):
    """
    Checks that the value entered by the user
    matches the available options.
    """
    # print("Validating meal choice...")

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

    if email not in guest_list:
        return False
    print("Welcome back! We already have your RSVP.")
    print("Your RSVP said:\n")

    return True


def find_a_row(value):
    """
    Finds a row with matching email string
    and return row number
    """
    row_with_guest = SHEET.worksheet("main").find(value)
    return row_with_guest.row


def return_response_details(value):
    """
    Reads values in header row and
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
    print("THANK YOU FOR USING THIS RSVP TOOL\n")
    print("Click RUN PROGRAM to run it again.")
    return


def confirm_rsvp():
    """
    Prints message to guest to confirm
    RSVP has been recorded and prints summary
    of their responses in terminal.
    """
    print("Thank you for letting us know!")
    print("We recorded your RSVP as follows:")

# Functions calculating totals start here


def increment_rsvp_count():
    """
    Converts string into integer and increments total number
    of reponses received in RSVP column
    on totals worksheet by 1;
    """
    rsvp_total_cell = int(SHEET.worksheet("totals").acell('B2').value)
    print(rsvp_total_cell)
    rsvp_total_cell += 1
    print(rsvp_total_cell)
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
        return yes_responses_cell
    elif value == "N":
        no_responses_cell = int(SHEET.worksheet("totals").acell('D2').value)
        no_responses_cell += 1
        update_selected_cell(2, 4, no_responses_cell)
        return no_responses_cell


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
    print("Calculating total of kids")
    print(sum_kids)
    print("Updating total kids column")
    update_selected_cell(2, 6, sum_kids)
    print(f"Total of kids attending: {sum_kids}")
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
    print("Calculating total of adults")
    print(sum_adults)
    print("Updating total adults column")
    update_selected_cell(2, 5, sum_adults)
    print(f"Total of adults attending: {sum_adults}")
    return sum_adults


def increment_meal_choice(value):
    """
    Increments total of selected meal option
    and updates total in the relevant column on
    total worksheet.
    """
    # print(f"Addin your meal choise: {value}")

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
    Calculate what percentage of responses
    has been received and rounds the result to 2 decimal places.
    """
    print("Calculating percentage")
    whole = int(SHEET.worksheet("totals").acell('A2').value)
    calc_percentage = float(value)/float(whole) * 100
    percentage = str(round(calc_percentage, 2)) + "%"
    update_selected_cell(2, 11, percentage)
    print("Finished calculating percentage!")
    print("All done!")
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
    selected_option = show_intro_options()
    run_selected_option(selected_option)

    if selected_option == "G":
        print_logo()
        guest_email = get_guest_info()
        # If email already on the worksheet, confirm
        # # RSVP recorded and end program
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
            # Only if guest responded Yes, show option to select meals
            if rsvp_response == "Y":
                meal_selected = get_diet()
                increment_meal_choice(meal_selected)
            
            add_guest(rsvp_info)
            count_adults()
            count_kids()
            rsvp_total = increment_rsvp_count()
            calculate_percentage(rsvp_total)
            increment_accept_or_decl(rsvp_response)
            confirm_rsvp()
            rsvp_row_number = find_a_row(guest_email)
            rsvp_summary = return_response_details(rsvp_row_number)
            print_rsvp_details(rsvp_summary)
            end_program()


main()

