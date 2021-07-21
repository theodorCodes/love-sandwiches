# Required libraries:
# Used this command to install python libraries
# pip3 install gspread google-auth

# After installation please import the following:
import gspread  # imports entire gspread library
from google.oauth2.service_account import Credentials
# imports the Google Credential class which is part of
# the service_account function from the Google auth library

# Below we need to define the SCOPE, which is part
# of the Google IAM (Identity and Access Management)
# configuration and specifies what the user has access to.
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')


# Test if the this file works with the Google API:
# sales = SHEET.worksheet('sales')
# data = sales.get_all_values()
# print(data)

# To run the test above, execute the following command in the Terminal
# while inside the project folder:
# python3 run.py
# Expected result: print of Google spreadsheet

# After testing, comment out the above test and move on to below code


def get_sales_data():
    """
    Get sales figures input from the user.
    Run a while loop to collect a valid string of data from the user
    via the terminal, which must be a string of 6 numbers separated
    by commas. The loop will repeatedly request data, until it is valid.
    The format that we're going to expect our values in is called csv.
    """
    # Creating while loop that request and validates correct data input
    # will break once the returned value in validate_data() is True
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        # Saving user entry as string
        data_str = input("Enter your data here: ")

        # Test log
        # print(f"The data provided is {data_str}")

        # Saving string data as comma seperated list with split() method
        sales_data = data_str.split(",")

        # Calling validate_data() function, passing 'sales_data' as argument
        # If the validate_data() function returns True break this loop
        # See return values (False/True) in the validate_data() function
        if validate_data(sales_data):
            print("Data is valid!")
            break

    # Return user input
    return sales_data


# Function that requires 1 parameter (values)
def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    """
    try:
        # Using list comprehension to loop through 'values'
        # and converting every item into an integer
        [int(value) for value in values]
        # Checking if length of 'values" is not 6
        if len(values) != 6:
            # If values not 6, give user error feedback
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    # Using 'as' keyword to create an error statement for value e
    # e stores the error value that we have specified above when
    # raising the ValueError
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        # Return Fals if input data is not valid
        return False

    # Return True if input data is valid
    return True


# def update_sales_worksheet(data):
#     """
#     Update sales worksheet, add new row with the list data provided
#     """
#     print("Updating sales worksheet...\n")
#     sales_worksheet = SHEET.worksheet("sales")
#     sales_worksheet.append_row(data)
#     print("Sales worksheet updated successfully.\n")


# def update_surplus_worksheet(data):
#     """
#     Update surplus worksheet, add new row with the list data provided
#     """
#     print("Updating surplus worksheet...\n")
#     surplus_worksheet = SHEET.worksheet("surplus")
#     surplus_worksheet.append_row(data)
#     print("Surplus worksheet updated successfully.\n")


# REFACTOR THE ABOVE 2 FUNCTIONS INTO ONE IN update_worksheet()
# where parameter worksheet is our sheet variable such as 'sales' or 'surplus'
# Function to update values to google spreadsheet
def update_worksheet(data, worksheet):
    """
    Receives a list of integers to be inserted into a worksheet
    Update the relevant worksheet with the data provided
    """
    # Giving feedback to user
    print(f"Updating {worksheet} worksheet...\n")
    # Setting our Google sheet as variable, using the
    # 'gspread worksheet()' method to access our sales worksheet
    worksheet_to_update = SHEET.worksheet(worksheet)
    # Update Goolge 'sales' worksheet by using append_row() method
    worksheet_to_update.append_row(data)
    # Giving feedback to user
    print(f"{worksheet} worksheet updated successfully\n")


# Function to retrieve 'stock' data and output surplus
def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.
    The surplus is defined as the sales figure subtracted from the stock:
    - Positive surplus indicates waste
    - Negative surplus indicates extra made when stock was sold out.
    """
    print("Calculating surplus data...\n")
    # Request row of data from Google 'stock' worksheet
    # using 'gspread" method .get_all_values()
    stock = SHEET.worksheet("stock").get_all_values()
    # Pulling the last row from sheet using Python slice [-1] technique
    stock_row = stock[-1]

    # Unpacking 2 rows of data for comparison
    # Creating empty list
    surplus_data = []
    # Using for loop and zip() method to iterate through 'stock' and 'sales' data
    # from Google spreadsheet at once, where stock_row represents
    # the last row in the 'stock' sheet and sales_row represents
    # the user input data.
    for stock, sales in zip(stock_row, sales_row):
        # Here we substract the stock from the sales row
        surplus = int(stock) - sales
        # and append the result to our empty list
        surplus_data.append(surplus)

    # Test log
    # print(surplus_data)

    return surplus_data


# Function to get last entries from the Google 'sales' sheet
# using gspread .col_values() method
def get_last_5_entries_sales():
    """
    Collects columns of data from sales worksheet, collecting
    the last 5 entries for each sandwich and returns the data
    as a list of lists.
    """
    # Access and store Google 'sales' sheet
    sales = SHEET.worksheet("sales")
    # Prepare empty list
    columns = []
    # Iterate through 6 columns starting from 1 as spreadsheet
    # columns start at 1 and not 0
    for ind in range(1, 7):
        # iterate each column in the sales sheet
        column = sales.col_values(ind)
        # append only the last 5 items of each column to columns
        columns.append(column[-5:])

    return columns


# Function to calculate the average from each list in our data
def calculate_stock_data(data):
    """
    Calculate the average stock for each item type, adding 10%
    """
    print("Calculating stock data...\n")
    new_stock_data = []

    # Using for loop to iterate through each column in our data
    for column in data:
        # Converting data to integers with list comprehension
        int_column = [int(num) for num in column]
        # Calculate the sum divided by the length of column
        average = sum(int_column) / len(int_column)
        # Here we add 10% to the average (as requested by marketing)
        stock_num = average * 1.1
        # Then we round, and add the results to the empty list
        new_stock_data.append(round(stock_num))

    return new_stock_data


# It's common practice to wrap the main function calls of
# a program within a function called main
def main():
    """
    Run all program functions
    """
    # Save user input from get_sales_data() in data
    data = get_sales_data()
    # Using list comprehension loop to convert strings into integers
    sales_data = [int(num) for num in data]
    # Update Google worksheet on the 'sales' sheet
    update_worksheet(sales_data, "sales")

    new_surplus_data = calculate_surplus_data(sales_data)
    # Update Google worksheet on the 'surplus' sheet
    update_worksheet(new_surplus_data, "surplus")
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    # Update Google worksheet on the 'stock' sheet
    update_worksheet(stock_data, "stock")


print("Welcome to Love Sandwiches Data Automation")
main()


"""
Note: Please use the Code Institute Stock Results Challenge for below code

Challenge:

1) Add your credentials to the creds.json file
2) Within main.py create a function named get_stock_values
3) The function should take a parameter named: data
4) Within the function create a variable named: headings.
5) Using what you have learned, reach out to your worksheet and retrieve the headings and assign them to the variable named: headings (this can be accomplished in a single line of code if you want to challenge yourself further)

With that done you will need to create a dictionary, using the headings values for the dictionary keys and the data values for the dictionary values and return this from your function.
This can be achieved by either creating a dictionary using a for loop, or by using a dictionary comprehension.
 
1) Create a variable named stock_values
2) Assign it the return value from calling the function get_stock_values and passing it in the variable named stock_data
3) Print the stock_data to the terminal, (This is for you to see the output and is not tested for)
"""


def get_stock_values(data):
    # headings = SHEET.worksheet("sales").row_values(1)
    # my_dict = dict(zip(headings, data))
    headings = SHEET.worksheet("sales").get_all_values()[0]
    return {headings[x]: data[x] for x in range(len(headings))}


stock_values = get_stock_values(stock_data)
print("Make the following numbers of sandwiches for next market:\n")
print(stock_values)

print(stock_data)
