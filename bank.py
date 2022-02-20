##########################################################################################################
##########################################################################################################
#
#   _____                         _____        __ _                          
#  / ____|                       / ____|      / _| |                         
# | |  __  ___  _ __  _______   | (___   ___ | |_| |___      ____ _ _ __ ___ 
# | | |_ |/ _ \| '_ \|_  / _ \   \___ \ / _ \|  _| __\ \ /\ / / _` | '__/ _ \
# | |__| | (_) | | | |/ / (_) |  ____) | (_) | | | |_ \ V  V / (_| | | |  __/
#  \_____|\___/|_| |_/___\___/  |_____/ \___/|_|  \__| \_/\_/ \__,_|_|  \___|
#
#                                                                            
#  Name: Shane Wilson
#  Creation Date: 10/12/2021      
#  Title: TU856/2 Object-Oriented Programming Assignment 
#  Description: This is a command-line banking system program written in Python 3 programming language.
#
##########################################################################################################
##########################################################################################################



############################################################
################## IMPORT MODULES ##########################
############################################################

import random
import secrets
import sys
from datetime import datetime, timedelta

############################################################
############## DEFINE GLOBAL VARIABLES #####################
############################################################

CUSTOMERS = "customers.txt"
ACCOUNTS = "accounts.txt"
TRANSACTIONS = "accountsTransactions.txt"
DATE_FORMAT = "%Y-%m-%d"


############################################################
############## DEFINE GLOBAL FUNCTIONS #####################
############################################################

def ReadCustomers(currentCustomer=None, filename=CUSTOMERS):
    """ This function opens the customers file, reads the file and splits each line into a list and stores them (nested) in another list, if current customer list is passed then ommit their details from the list"""
    customer_list = []
    with open(filename, "r") as file:
        for line in file:
            line = line.rstrip()
            if line and line != currentCustomer:
                customer_list.append(line.strip().split(','))
    file.close()
    return customer_list

def StoreCustomer(customerNo, customers_list):
    """ This function checks if a customer matches passed customerNo value then returns that customers details list"""
    customer_details = False
    for customer in customers_list:
        if int(customer[0]) == customerNo:
            customer_details = customer
    return customer_details

def ReadTransactions(accNo=None,filename=TRANSACTIONS):
    """ This function opens the tranactions file, reads the file and splits each line into a list of transactions associated with an account number and stores them (nested) in another list"""
    transaction_list_full = []
    transaction_list = []
    with open(filename, "r") as file:
        for line in file:
            line = line.rstrip()
            if line:
                transaction_list_full.append(line.strip().split(','))
    file.close()
    if accNo != None:
        for transaction in transaction_list_full:
            if transaction[0] == accNo or transaction[1] == accNo:
                transaction_list.append(transaction)
        return transaction_list
    else: 
        return transaction_list_full

def line_generator(characters:str, chartype="#"):
    """This function takes a string as an argument, counts the characters and returns that many # characters as styling lines above and below the string"""
    amount =""
    for i in range(0, characters.__len__()):
        amount += chartype

    return f"\n{amount}\n{characters}\n{amount}\n"


############################################################
############### GENERAL ACCOUNT CLASS ######################
############################################################


class Account(object):
    """ This class is the main account handling class, it holds all of an accounts information and has withdraw, deposit, transfer and delete account methods"""

########### Class attribute initialization ###########
    def __init__(self, customerid, accNo, accType, balance, status, limit, lastupdate):
        self.customerid = customerid
        self.accType = accType
        self.accNo = accNo
        self.balance = int(balance)
        self.status = status
        self.limit = limit
        self.lastupdate = lastupdate

########### Withdraw method ###########
    def withdraw(self, amount):
        """This function validates a withdrawal, updates account object balance, writes the transaction to transactions.txt and writes the changes to accounts.txt"""
        if amount <= 0:
            return line_generator("You can only withdraw a positive value")
        if self.balance-amount < int(self.limit):
            return line_generator("You do not have enough funds to complete this transaction and/or this transaction will exceed your credit limit.")
        
        # Get todays date
        today = datetime.today()

        # Store the accounts last update date
        lastupdate = datetime.strptime(self.lastupdate, DATE_FORMAT)

        # Calculate days since last update
        days_since_lastupdate = today - lastupdate

        # If the account is a savings account and the last transaction was less than 30 days ago, display an error
        if self.accType == "2" and days_since_lastupdate.days < 30:
            days_remaining = 30 - days_since_lastupdate.days
            return line_generator("You cannot withdraw or transfer from this account for another " + str(days_remaining) + " days.")

        # Set the transaction type
        transactiontype = "withdraw"

        # Store the account as a list
        account_list = [str(self.customerid), str(self.accNo), str(self.accType), str(self.balance), str(self.status), str(self.limit), str(self.lastupdate)]

        # Store the account as a string
        account_str =  str(account_list[0]) + "," + str(account_list[1]) + "," + str(account_list[2]) + "," + str(account_list[3]) + "," + str(account_list[4]) + "," + str(account_list[5]) + "," + str(account_list[6])
        
        # Subtract the withdrawal from the accounts balance attribute
        self.balance -= amount

        # Set the new update date to todays date
        self.lastupdate = datetime.today().strftime(DATE_FORMAT)

        # Read in the transactions file
        with open(TRANSACTIONS, 'a') as file :

            # Create a transaction ID
            txid = secrets.token_hex(15)

            # Create a transaction f string
            deposit_transaction = f"\n{self.accNo},{self.accNo},{transactiontype},{amount},{txid}"

            # Append the transaction to file
            file.write(deposit_transaction)

        # Read in the accounts file
        with open(ACCOUNTS, 'r') as file :
            filedata = file.read()

            # Set the 3rd element in the account list to the new balance
            account_list[3] = self.balance

            # If the account is a savings account, update the 6th element in the account list to the new update date
            if account_list[2] == "2":
                account_list[6] = self.lastupdate
            
            # Store the new account as a string
            newaccount = str(account_list[0]) + "," + str(account_list[1]) + "," + str(account_list[2]) + "," + str(account_list[3]) + "," + str(account_list[4]) + "," + str(account_list[5]) + "," + str(account_list[6])
            
            # Replace the old account string with the new account string
            filedata = filedata.replace(account_str, newaccount)

        # Write the file out again
        with open(ACCOUNTS, 'w') as file:
            file.write(filedata)

        # Return success message
        return line_generator("Withdrawal Successful")

########### Deposit method ###########
    def deposit(self, amount):
        """This function validates a deposit, updates account object balance, writes the transaction to transactions.txt and writes the changes to accounts.txt"""

        # If the amount is a negative value, return error
        if amount <= 0:
            return line_generator("You can only deposit a positive value")

        # Set the transaction type
        transactiontype = "deposit"

        # Store the account as a list
        account_list = [str(self.customerid), str(self.accNo), str(self.accType), str(self.balance), str(self.status), str(self.limit), str(self.lastupdate)]

        # Store the account as a string
        account_str =  str(account_list[0]) + "," + str(account_list[1]) + "," + str(account_list[2]) + "," + str(account_list[3]) + "," + str(account_list[4]) + "," + str(account_list[5]) + "," + str(account_list[6])
        
        # Add the deposit to the accounts balance attribute
        self.balance += amount

        # Read in the transactions file
        with open(TRANSACTIONS, 'a') as file:

            # Create a transaction ID
            txid = secrets.token_hex(15)

            # Create a transaction f string
            deposit_transaction = f"\n{self.accNo},{self.accNo},{transactiontype},{amount},{txid}"

            # Append the transaction to file
            file.write(deposit_transaction)

        # Read in the accounts file
        with open(ACCOUNTS, 'r') as file :
            filedata = file.read()

            # Set the 3rd element in the account list to the new balance
            account_list[3] = self.balance

            # Store the new account as a string
            newaccount = str(account_list[0]) + "," + str(account_list[1]) + "," + str(account_list[2]) + "," + str(account_list[3]) + "," + str(account_list[4]) + "," + str(account_list[5]) + "," + str(account_list[6])
            
            # Replace the old account string with the new account string
            filedata = filedata.replace(account_str, newaccount)

        # Write the file out again
        with open(ACCOUNTS, 'w') as file:
            file.write(filedata)

        # Return success message
        return line_generator("Deposit Successful")
    
########### Transfer method ###########    
    def transfer(self, amount, receiveaccount):
        """This function validates a transfer, updates both account objects balances, writes the transaction to transactions.txt and writes the changes to accounts.txt"""

        # If the amount is a negative value, return error
        if amount <= 0:
            return line_generator("You can only transfer a positive value")

        # If the account balance minus the amount is less than the credit limit, return error
        if self.balance-amount < int(self.limit):
            return line_generator("You do not have enough funds to complete this transaction.")

        # Get todays date
        today = datetime.today()

        # Store the accounts last update date
        lastupdate = datetime.strptime(self.lastupdate, DATE_FORMAT)

        # Calculate days since last update
        days_since_lastupdate = today - lastupdate

        # If the account is a savings account and the last transaction was less than 30 days ago, display an error
        if self.accType == "2" and days_since_lastupdate.days < 30:
            days_remaining = 30 - days_since_lastupdate.days
            return line_generator("You cannot withdraw or transfer from this account for another " + str(days_remaining) + " days.")

        # Set the transaction type
        transactiontype = "transfer"

        # Store the account as a list
        account_list = [str(self.customerid), str(self.accNo), str(self.accType), str(self.balance), str(self.status), str(self.limit), str(self.lastupdate)]

        # Store the account as a string
        account_str =  str(account_list[0]) + "," + str(account_list[1]) + "," + str(account_list[2]) + "," + str(account_list[3]) + "," + str(account_list[4]) + "," + str(account_list[5]) + "," + str(account_list[6])

        # Create an Account instance for the receiver account
        receiver = Account(receiveaccount[0], receiveaccount[1], receiveaccount[2], receiveaccount[3], receiveaccount[4], receiveaccount[5], receiveaccount[6])

        # If the sender and receiver account numbers match, return error
        if self.accNo == receiver.accNo:
            return line_generator("You cannot transfer to the same account")

        # Store the receiver account as a string
        receiver_str = str(receiveaccount[0]) + "," + str(receiveaccount[1]) + "," + str(receiveaccount[2]) + "," + str(receiveaccount[3]) + "," + str(receiveaccount[4]) + "," + str(receiveaccount[5]) + "," + str(receiveaccount[6])
        
        # Subtract the amount from the senders balance attribute
        self.balance -= amount
        
        # Add the amount to the receivers balance attribute
        receiver.balance += amount
        
        # Set the new update date to todays date for the senders account
        self.lastupdate = datetime.today().strftime(DATE_FORMAT)

        # Add transaction to transactions file
        with open(TRANSACTIONS, 'a') as file:

            # Create a transaction ID
            txid = secrets.token_hex(15)

            # Create a transaction f string
            transfer_transaction = f"\n{self.accNo},{receiveaccount[1]},{transactiontype},{amount},{txid}"

            # Append the transaction to file
            file.write(transfer_transaction)

        # Read in the accounts file
        with open(ACCOUNTS, 'r') as file:
            senderfiledata = file.read()

            # Set the 3rd element in the senders account list to the new balance
            account_list[3] = self.balance

            # If the account is a savings account, update the 6th element in the account list to the new update date
            if account_list[2] == "2":
                account_list[6] = self.lastupdate
            
            # Store the new account as a string
            newaccount = str(account_list[0]) + "," + str(account_list[1]) + "," + str(account_list[2]) + "," + str(account_list[3]) + "," + str(account_list[4]) + "," + str(account_list[5]) + "," + str(account_list[6])
            
            
            # Replace the old account string with the new account string
            senderfiledata = senderfiledata.replace(account_str, newaccount)

        # Write the file out again
        with open(ACCOUNTS, 'w') as file:
            file.write(senderfiledata)


        # Read in the accounts file
        with open(ACCOUNTS, 'r') as file :
            receiverfiledata = file.read()

            # Set the 3rd element in the receivers account list to the new balance
            receiveaccount[3] = receiver.balance

            # Store the new account as a string
            newaccount = str(receiveaccount[0]) + "," + str(receiveaccount[1]) + "," + str(receiveaccount[2]) + "," + str(receiveaccount[3]) + "," + str(receiveaccount[4]) + "," + str(receiveaccount[5]) + "," + str(receiveaccount[6])
            
            # Replace the old account string with the new account string
            receiverfiledata = receiverfiledata.replace(receiver_str, newaccount)

        # Write the file out again
        with open(ACCOUNTS, 'w') as file:
            file.write(receiverfiledata)

        # Return success message
        return line_generator("Transfer Successful")

########### Delete account method ###########
    def DeleteAccount(self):
        """This function deletes an account by updatings it's status attribute from 0 to 1 then writing the changes to accounts.txt"""

        # Store the account as a list
        account_list = [str(self.customerid), str(self.accNo), str(self.accType), str(self.balance), str(self.status), str(self.limit), str(self.lastupdate)]

        # Store the account as a string
        account_str =  str(account_list[0]) + "," + str(account_list[1]) + "," + str(account_list[2]) + "," + str(account_list[3]) + "," + str(account_list[4]) + "," + str(account_list[5]) + "," + str(account_list[6])
        
        # Read in the file
        with open(ACCOUNTS, 'r') as file :
            filedata = file.read()

            # Set the 4th element in the account list to 1
            account_list[4] = "1"

            # Store the new account as a string
            newaccount = str(account_list[0]) + "," + str(account_list[1]) + "," + str(account_list[2]) + "," + str(account_list[3]) + "," + account_list[4] + "," + str(account_list[5]) + "," + str(account_list[6])
            
            # Replace the old account string with the new account string
            filedata = filedata.replace(account_str, newaccount)

        # Write the file out again
        with open(ACCOUNTS, 'w') as file:
            file.write(filedata)

        # Return true
        return True


########### String method ###########
    def __str__(self):
        result = "Customer ID: " + str(self.customerid) + "\n"
        result += "Account Number: " + str(self.accNo) + "\n"
        if self.accType == 1:
            result += "Account Type: Checking Account\n"
        else:
            result += "Account Type: Savings Account\n"
        result += "Balance: " + str(self.balance) + "\n"
        if self.status == "0":
            result += "Status: Open\n"
        else:
            result += "Status: Closed\n"
        result += "Credit Limit: " + str((int(self.limit)*-1)) + "\n"
        return result


############################################################
############# SAVINGS ACCOUNT CLASS ########################
############################################################

class SavingAccount(Account):
    """The SavingAccount class is a subclass of the Account class, it has one method, and it is for adding new savings accounts."""

########### Class attribute initialization ###########    
    def __init__(self, customerID, accNo, balance=0, status=0, accType=2, limit=0):
        self.accNo = accNo
        self.accType = accType
        self.balance = balance
        self.customerID = customerID
        self.status = status
        self.limit = limit
        days_30 = datetime.today() - timedelta(days=31)
        self.today = days_30.strftime(DATE_FORMAT)

########### Add new account method ###########
    def AddAccount(self, filename=ACCOUNTS):
        """This function creates an f string of the new account details and writes it to accounts.txt"""

        file = open(filename, "a")
        saving_account = f"\n{self.customerID},{self.accNo},{self.accType},{self.balance},{self.status},{self.limit},{self.today}"
        if(file.write(saving_account)):
            file.close()
            return True
        else:
            file.close()
            return False
    
########### String method ###########
    def __str__(self):
        result = "Customer ID: " + str(self.customerid) + "\n"
        result += "Account Number: " + str(self.accNo) + "\n"
        result += "Account Type: Savings Account\n"
        result += "Balance: " + str(self.balance) + "\n"
        if self.status == "0":
            result += "Status: Open\n"
        else:
            result += "Status: Closed\n"
        result += "Credit Limit: " + str((int(self.limit)*-1)) + "\n"
        return result


############################################################
############# CHECKING ACCOUNT CLASS #######################
############################################################

class CheckingAccount(Account):
    """The CheckingAccount class is a subclass of the Account class, it has one method, and it is for adding new checking accounts."""

########### Class attribute initialization ###########    
    def __init__(self, customerID, accNo, balance=0, status=0, accType=1, limit=-1000):
        self.accNo = accNo
        self.accType = accType
        self.balance = balance
        self.customerID = customerID
        self.status = status
        self.limit = limit
        days_30 = datetime.today() - timedelta(days=31)
        self.today = days_30.strftime(DATE_FORMAT)

########### Add new account method ###########
    def AddAccount(self, filename=ACCOUNTS):
        """This function creates an f string of the new account details and writes it to accounts.txt"""

        file = open(filename, "a")
        checking_account = f"\n{self.customerID},{self.accNo},{self.accType},{self.balance},{self.status},{self.limit},{self.today}"
        if(file.write(checking_account)):
            file.close()
            return True
        else:
            file.close()
            return False

########### String method ###########
    def __str__(self):
        result = "Customer ID: " + str(self.customerid) + "\n"
        result += "Account Number: " + str(self.accNo) + "\n"
        result += "Account Type: Checking Account\n"
        result += "Balance: " + str(self.balance) + "\n"
        if self.status == "0":
            result += "Status: Open\n"
        else:
            result += "Status: Closed\n"
        result += "Credit Limit: " + str((int(self.limit)*-1)) + "\n"
        return result


############################################################
############# CUSTOMER INFORMATION CLASS ###################
############################################################

class Customer(object):
    """This is the Customer class, it has 3 methods, AddCustomer, ViewAccounts and ViewOtherAccounts"""

########### Class attribute initialization ###########
    def __init__(self, customerID, fname, sname, age):
        self.fname = fname
        self.sname = sname
        self.age = age
        self.customerID = customerID

########### Create new customer account method ###########
    def AddCustomer(self, filename=CUSTOMERS):
        """This function creates an f string of the new customers details and writes it to customers.txt"""

        file = open(filename, "a")
        customer_account = f"\n{self.customerID},{self.fname},{self.sname},{self.age}"
        if(file.write(customer_account)):
            file.close()
            return True
        else:
            file.close()
            return False

########### View own method ###########    
    def ViewAccounts(self, filename=ACCOUNTS):
        """This function reads accounts.txt and stores each line as a nested list, then finds all accounts with a customers ID and stores them in another list of lists"""

        account_list = []
        user_accounts = []
        with open(filename, "r") as file:
            for account in file:
                account = account.rstrip()
                if account:
                    account_list.append(account.strip().split(','))
        file.close()
        for accounts in account_list:
            i = 0
            if accounts[0] == self.customerID and accounts[4] == "0":
                user_accounts.append(accounts)
            i += 1
        return user_accounts

########### View other accounts method ###########    
    def ViewOtherAccounts(self, othercustomerid, filename=ACCOUNTS):
        """This function reads accounts.txt and stores each line as a nested list, then finds all accounts with another customers ID and stores them in another list of lists"""

        account_list = []
        user_accounts = []
        with open(filename, "r") as file:
            for account in file:
                account = account.rstrip()
                if account:
                    account_list.append(account.strip().split(','))
        file.close()
        for accounts in account_list:
            i = 0
            if accounts[0] == othercustomerid and accounts[0] != self.customerID and accounts[4] == "0":
                user_accounts.append(accounts)
            i += 1
        return user_accounts

########### String method ###########
    def __str__(self):
        result = "Customer ID: " + str(self.customerID) + "\n"
        result += "Customer Name: " + str(self.fname) + str(self.sname) + "\n"
        result += "Customer Age: " + str(self.age) + "\n"
        return result



############################################################
################# MAIN MENU FUNCTION #######################
############################################################

def menu():
    """This is the main menu function."""

    # Display the main menu options
    print(line_generator("Welcome to TUD Bank!", "|"))
    print(line_generator("Please choose one of the following options.", "="))
    print(line_generator("1. Open New Account \n2. Manage Existing Accounts", "="))

    # Get user selection input
    menuOption = input("\n Please choose an option or enter [x] to exit: \n")

    # Open new account option
    if menuOption == "1":

        # Create new account menu function
        def newAccount():
            """This is the new account menu function."""

            # Display the new account menu options
            print(line_generator("Open New Account", "="))
            print(line_generator("Please choose one of the following options.", "="))
            print(line_generator("1. New Customer \n2. Existing Customer ", "="))

            # Get user selection input
            newAccOption = input("\nPlease choose an option or enter [x] to return to main menu: \n")

            # If user selects option 1, the user is a new customer so, gather their details from input, generate a random customer ID, create new customer object and run the add account method on the object
            if(newAccOption == "1"):
                fname = input("Please enter your first name: ")
                sname = input("Please enter your last name: ")
                age = input("Please enter your age: ")
                new_custid = random.randint(1000000000,9999999999)
                new_customer = Customer(new_custid, fname, sname, age)
                new_customer.AddCustomer()

                # If successful, display the users new customer ID, else display error
                if(new_customer):
                    print(line_generator("Your customer account has been created, your unique customer ID is: " + str(new_custid)))
                else:
                    print(line_generator("There was an error creating your customer account, please try again later."))
                   
            # If user selects option 2, the user is an existing customer, so ask user to enter their customer ID. Pass the ID to the Read
            elif(newAccOption == "2"):
                customerNo = int(input("\n Please enter your customer number: \n"))
                customers_list = ReadCustomers()
                customer_details = StoreCustomer(customerNo, customers_list)

                # If a customer is returned from the database file (customers.txt) then create a customer object and ask which type of account user would like to open
                if(customer_details):
                    customer = Customer(customer_details[0], customer_details[1], customer_details[2], customer_details[3])

                    # Ask user what type of account they would like to open, and store their selection in variable
                    accountTypeOption = input("\n What type of account would you like to open?\n 1. Checking Account\n 2. Savings Account \n\n Enter [x] to cancel\n\n")

                    # If user selects option 1, pass the customers information from customer instance to the checking account class and run the add account method
                    if(accountTypeOption == "1"):
                        if(int(customer.age) > 17):
                            new_acc_no = random.randint(1000000000,9999999999)
                            new_acc = CheckingAccount(customer.customerID, new_acc_no)
                            new_acc.AddAccount()
                            if(new_acc):
                                print(line_generator("Your new checking account number is: " + str(new_acc_no)))
                            else:
                                print(line_generator("There was an error setting up your account, please try again later."))
                        else:
                            print(line_generator("Sorry, you must be 18 or older to open a checking account."))

                    # If user selects option 1, pass the customers information from customer instance to the savings account class and run the add account method
                    elif(accountTypeOption == "2"):
                        if(int(customer.age) > 13):
                            new_acc_no = random.randint(1000000000,9999999999)
                            new_acc = SavingAccount(customer.customerID, new_acc_no)
                            new_acc.AddAccount()
                            if(new_acc):
                                print(line_generator("Your new savings account number is: " + str(new_acc_no)))
                            else:
                                print(line_generator("There was an error setting up your account, please try again later."))
                        else:
                            print(line_generator("Sorry, you must be 14 or older to open a savings account."))

                    # Exit this menu and return to previous menu
                    elif(accountTypeOption == "x"):
                        newAccOption = "2"
                    else:
                        print(line_generator("ERROR: That is not a valid option. Please try again."))

                else:
                    print(line_generator("Customer not found"))

            elif(newAccOption == "x"):
                print(line_generator("Returning to main menu"))
            else:
                print(line_generator("ERROR: That is not a valid option. Please try again."))
            return newAccOption

        ############################################################
        ############# NEW ACCOUNT MENU FUNCTION CALL ###############
        ############################################################

        # Run new account menu function
        newAccOption = newAccount()

        # Loop only exits when user selects option 3
        while newAccOption != "x":
            newAccOption = newAccount()
    
    # Manage existing account option
    elif menuOption == "2":

        # Ask user to enter a customer number, if they do not enter an integer then display an error
        try:
            customerNo = int(input("\n Please enter your customer number: \n"))
        except ValueError:
            customerNo = "x"
            print(line_generator("You did not enter a valid integer."))

        if customerNo != "x":

            # Get all customer details into a list of lists using ReadCustomer()
            customers_list = ReadCustomers()

            # Store current customers details
            customer_details = StoreCustomer(customerNo, customers_list)

            # If a customer was found amd customer_details list was created then continue
            if(customer_details):

                # Create a Customer instance
                customer = Customer(customer_details[0], customer_details[1], customer_details[2], customer_details[3])

                # Store their accounts in a list of lists
                account_list = customer.ViewAccounts()

                # Set account to be empty
                account = None

                # Start our counter at 1
                i = 1

                # Check if the account list has any accounts and if it does then display them as options for the user to select
                if len(account_list):
                    print(line_generator("Please choose which account you would like to manage: "))
                    print("OPTION   |   ACCOUNT NO.  |   ACCOUNT TYPE   |   BALANCE\n")
                    for account in account_list:
                        if  int(account[4]) == 0:
                            if int(account[2]) == 1:
                                account_type = "Checking"
                            else:
                                account_type = "Savings "
                            print(i, " |   ", account[1], " |   ", account_type, " |   ", account[3])
                            i += 1
                    
                    # Ask the user to select an account
                    try:
                        account_selection = int(input("\n Please enter your selection: \n"))
                    except ValueError:
                        account_selection = "x"
                        print(line_generator("You did not enter a valid integer."))
                    
                    # If the user selected a valid account, create an account instance with the account details
                    if account_selection != "x":

                        # Start counter at 1
                        i = 1

                        for accounts in account_list:
                            if i == account_selection:
                                select_account = Account(accounts[0], accounts[1], accounts[2], accounts[3], accounts[4], accounts[5], accounts[6])
                            i += 1
                    
                    # If the instance was created, run the manage account menu
                    if(select_account):
                        def manageAccount(select_account):
                            """This is the manage account function"""

                            # Display the menu options
                            print(line_generator("Account Management", "="))
                            print(line_generator("Please choose one of the following options.", "="))
                            print(" 1. View Account Information \n 2. View Transactions \n 3. View Balance \n 4. View Credit Limit \n 5. Deposit \n 6. Withdraw \n 7. Transfer \n 8. Close Account")

                            # Get user selection input
                            accountOption = input("\n Please choose an option or enter [x] to return to previous menu: \n")

                            # Display account information
                            if accountOption == "1":
                                print('\n#############################\n\nAccount Information \n')
                                print(select_account)
                                print('#############################\n')

                            # Display account transactions
                            elif accountOption == "2":
                                transactions = ReadTransactions(select_account.accNo)

                                # Start counter at 1
                                i = 1

                                print(line_generator("Transactions", "="))
                                print(line_generator("ID   |   Type     |   Amount", "="))
                                for transaction in transactions:
                                    print(str(i) + "    |   " + str(transaction[2]) + "  |   " + str(transaction[3]))
                                    i += 1
                                print("\n#######################################\n")
                            
                            # Display account balance
                            elif accountOption == "3":
                                print(line_generator("Account balance: " + str(select_account.balance)))

                            # Display account credit limit
                            elif accountOption == "4":
                                positive_limit = int(select_account.limit) * -1
                                print(line_generator("Account credit limit: " + str(positive_limit)))
                            
                            # Deposit to account
                            elif accountOption == "5":
                                try:
                                    amount = int(input("\n Please enter amount to deposit: \n"))
                                    print(select_account.deposit(amount))
                                except ValueError:
                                    print(line_generator("Please enter a valid integer"))
                            
                            # Withdraw from account
                            elif accountOption == "6":
                                try:
                                    amount = int(input("\n Please enter amount to withdraw: \n"))
                                    print(select_account.withdraw(amount))
                                except ValueError:
                                    print(line_generator("Please enter a valid integer"))
                            
                            # Transfer to another account
                            elif accountOption == "7":

                                # Add the current customers details to a string for searching customers.txt
                                currentCustomer = str(customer.customerID) + "," + str(customer.fname) + "," + str(customer.sname) + "," + str(customer.age) 

                                # Get a list of other customers using ReadCustomers function
                                customers_transfer_list = ReadCustomers(currentCustomer)

                                # Print table header
                                print(line_generator("Please choose which customer you would like to transfer to: "))
                                print("OPTION   |   CUSTOMER NAME\n")

                                # Start counter at 1
                                i = 1

                                # Loop through customers_transfer_list and display to user
                                for customers in customers_transfer_list:
                                    print(i, " |   ", customers[1], " ", customers[2])
                                    i += 1
                                
                                # Start counter at 1
                                i = 1

                                # Ask user to choose a customer, store selection in sendcustomer
                                customer_selection = input("\n Please choose a customer: \n")
                                for customers in customers_transfer_list:
                                    if i == int(customer_selection):
                                        sendcustomer = str(customers[0])
                                    i += 1
                                
                                # If the user selected a valid customer, display that customers account list
                                if sendcustomer:
                                    otheraccounts = customer.ViewOtherAccounts(sendcustomer)
                                    i = 1
                                    for others in otheraccounts:
                                        if  int(others[4]) == 0:
                                            if int(others[2]) == 1:
                                                account_type = "Checking"
                                            else:
                                                account_type = "Savings "
                                            print(i, " |   ", others[1], " |   ", account_type)
                                            i += 1

                                    # Ask user to select an account
                                    send_account_selection = int(input("\n Please choose account: \n"))

                                    # Start counter at 1
                                    i = 1

                                    # Set sendaccount to be false
                                    sendaccount = False

                                    # Loop through the selected customers accounts and find the selected account, store it as a list
                                    for otheraccount in otheraccounts:
                                        if i == send_account_selection:
                                            sendaccount = [str(otheraccount[0]), str(otheraccount[1]), str(otheraccount[2]), str(otheraccount[3]), str(otheraccount[4]), str(otheraccount[5]), str(otheraccount[6])]
                                        i += 1

                                    # If the user selected a valid account and sendaccount does not equal false, ask the user to enter an amount to transfer
                                    if sendaccount:
                                        amount = input("\n Please enter amount to transfer: \n")
                                        if amount.isnumeric():
                                            print(select_account.transfer(int(amount), sendaccount))
                                        else:
                                            print(line_generator("ERROR: Please enter a valid amount."))
                                    else:
                                        print(line_generator("Invalid selection, account not found"))
                                
                                else:
                                    print(line_generator("Invalid selection, customer not found"))
                            
                            # Delete account
                            elif accountOption == "8":
                                confirm = input("Are you sure you would like to delete this account? y/n\n")
                                if confirm == "y":
                                    delete = select_account.DeleteAccount()
                                    if delete:
                                        print(line_generator("Account deletion successful!"))
                                        accountOption = "x"
                                    else:
                                        print(line_generator("Error deleting account, please try again!"))
                                else:
                                    print(line_generator("Account deletion cancelled."))
                            
                            # Exit to previous menu
                            elif accountOption == "x":
                                print("Account Exit")
                                select_account = None
                            else:
                                print(line_generator("ERROR: That is not a valid option. Please try again."))
                            return accountOption
                        
                        # Loop to display manage account menu
                        accountSelection = manageAccount(select_account)
                        while accountSelection != "x":
                            accountSelection = manageAccount(select_account)

                    else:
                        print(line_generator("You do not have any active accounts with TUD bank, please open a new account to proceed."))
            else:
                print(line_generator("ERROR: Account not found."))
    
    # Exit program
    elif menuOption == "x":
        print("Program Exit")
    else:
        print(line_generator("ERROR: That is not a valid option. Please try again."))
    return menuOption

# Run main menu function
mainMenu = menu()

# Loop to display main menu
while mainMenu != "x":
    mainMenu = menu()
