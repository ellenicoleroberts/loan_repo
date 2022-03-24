#imports
from pathlib import Path
import csv
import fire
import questionary
from qualifier.utils.fileio import load_csv
from qualifier.utils.calculators import calculate_monthly_debt_ratio, calculate_loan_to_value_ratio
from qualifier.filters.max_loan_size import filter_max_loan_size


# This function loads a CSV file with the list of banks and available loans information
# from the file defined in `file_path`
def load_bank_data():
    file_path = questionary.text("Enter a file path to a rate-sheet (.csv):").ask()
    csvpath = Path(file_path)
    return load_csv(csvpath)

# As a lender,
# I want to filter the bank list by checking if the customer's credit score is equal to or greater than the minimum allowed credit score defined by the bank
# so that we can know which banks are willing to offer a loan to the customer
def filter_credit_score(credit_score, bank_list):
    credit_score_approval_list = []
    for bank in bank_list:
        if credit_score >= int(bank[4]):
            credit_score_approval_list.append(bank)
    return credit_score_approval_list


# @TODO Define a function that implements the following user story:
# As a lender,
# I want to filter the bank list by checking if the customer's debt-to-income is equal to or less than the maximum debt-to-income ratio allowed by the bank
# so that we can assess if the customer will have payment capacity according to the bank's criteria
def filter_debt_to_income(monthly_debt_ratio, bank_list):
    debt_to_income_approval_list = []
    for bank in bank_list:
        if monthly_debt_ratio <= float(bank[3]):
            debt_to_income_approval_list.append(bank)
    return debt_to_income_approval_list


# @TODO Define a function that implements the following user story:
# As a lender,
# I want to filter the bank list by checking if the customer's loan-to-value is equal to or less than the maximum loan-to-value ratio allowed by the bank
# so that we assess if the customer's home value is worth as an asset to secure the loan
def filter_loan_to_value(loan_to_value_ratio, bank_list):
    loan_to_value_approval_list = []

    for bank in bank_list:
        if loan_to_value_ratio <= float(bank[2]):
            loan_to_value_approval_list.append(bank)
    return loan_to_value_approval_list

def get_applicant_info():

    credit_score = questionary.text("What is your credit score?").ask()
    message = "Please enter a positive number."
    credit_score = int(credit_score)
    if credit_score >= 0:
        message = "Thank you."
    print(message)

    debt = questionary.text("How much debt do you have?").ask()
    message = "Please enter a positive number."
    debt = float(debt)
    if credit_score >= 0:
        message = "Thank you."
    print(message)

    income = questionary.text("What is your yearly income?").ask()
    message = "Please enter a positive number."
    income = float(income)
    if income >= 0:
        message = "Thank you."
    print(message)

    loan_amount = questionary.text("What is your loan amount you desire?").ask()
    message = "Please enter a positive number."
    loan_amount = float(loan_amount)
    if loan_amount >= 0:
        message = "Thank you."
    print(message)

    home_value = questionary.text("What is the value of the home you wish to buy?").ask()
    message = "Please enter a positive number."
    home_value = float(home_value)
    if home_value >= 0:
        message = "Thank you."
    print(message)
    return credit_score, debt, income, loan_amount, home_value
    
# This function implements the following user story:
# As a customer,
# I want to know what are the best loans in the market according to my financial profile
# so that I can choose the best option according to my needs
def find_qualifying_loans(bank_data, credit_score, debt, income, loan, home_value):
    # Calculate the monthly debt ratio
    monthly_debt_ratio = calculate_monthly_debt_ratio(debt, income)
    print(f"The monthly debt to income ratio is {monthly_debt_ratio:.02f}")

    # Calculate loan to value ratio
    loan_to_value_ratio = calculate_loan_to_value_ratio(loan, home_value)
    print(f"The loan to value ratio is {loan_to_value_ratio:.02f}.")

    # Run qualification filters
    bank_data_filtered = filter_max_loan_size(loan, bank_data)
    bank_data_filtered = filter_credit_score(credit_score, bank_data_filtered)
    bank_data_filtered = filter_debt_to_income(monthly_debt_ratio, bank_data_filtered)
    bank_data_filtered = filter_loan_to_value(loan_to_value_ratio, bank_data_filtered)

    print(f"Found {len(bank_data_filtered)} qualifying loans")

    return bank_data_filtered

# This function is the main execution point of the application. It triggers all the business logic.
def run():
    # Set the file path of the CVS file with the banks and loans information
    #file_path = "daily_rate_sheet.csv"
    # Load the latest Bank data
    bank_data = load_bank_data()

    # Get the applicant's information
    credit_score, debt, income, loan_amount, home_value = get_applicant_info()

    # Find qualifying loans
    qualifying_loans = find_qualifying_loans(
        bank_data, credit_score, debt, income, loan_amount, home_value
    )

    # Print the list of qualifying loans
    print(qualifying_loans)

if __name__ == "__main__":
    fire.Fire(run)
