# TUD-OOP-semester-1-CA
TU Dublin - Object Oriented Programming Semester 1 CA - Create a banking system using python.


# PROBLEMS DESCRIPTION:

You are asked to develop an application to manage bank services. An account is a general
account class that contains balance, deposit, transfer (send money to another account in
the bank) and withdrawal methods. Your bank should allow the creation of two bank
accounts types. The two types of accounts should include:
● Savings accounts: these only allow one withdrawal or one transfer per month, and
might also be opened by teenagers from 14 years old.
● Checking accounts: these are regular accounts that can be opened by customers who
are 18 years or older. They can also have a negative balance to a specified credit limit.
All the bank information should be stored in three external files: customers.txt,
accounts.txt, accountsTransactions.txt. It is up to you to define the structure of
each file, but each customer, account or transaction should have an unique ID.
Use Python classes to implement the bank system. Some of the functionality your system
should provide includes:
● At least the following classes: Account, Saving Account, Checking Account, Customer.
● Saving Account and Checking Account should be a subclass of Account.
● Each class should have an __init__ and __str__ methods. For each __str__ method,
think what information each class should provide when you print their instances.
● Persistent memory: when you start your system it should read the files
customers.txt, accounts.txt, and accountsTransactions.txt in the same
folder as the python code and create all the necessary instances.
● Provide a command line interface for the user to:
○ Customer creating a new account.
○ Customer viewing the transactions performed in one of his accounts and the
respective balance.
○ Customer performing the operations allowed by its account type.
○ Customer deletes his/her account.
○ Make sure to update the external files after any information is modified.
HINTS AND GENERAL GUIDELINES:
● Start with the easy parts. Define only your constructors and add new functionalities
one by one.
● Once a method has been coded test it before moving on to the next part
● Make sure you include any relevant error checking and handle unexpected input
● Make sure to use function annotations
● Once you have defined a class you can use its instances as any other type.
Remember to use composition, aggregation and inheritance if applicable.
● The easiest way to update external files is likely to write content to a new file and
replace the old file with the new file. To remove a file use the ‘remove’ function from
the ‘os’ module.
● Think about which data structure is more appropriate to the pieces of information you
need to store: list, string, dictionary, tuple, etc.
● Think if each attribute needs to be private or public. Remember to add get/set
methods for private attributes that are accessed outside the class.
● Add docstrings to all your classes and methods
● After implementing a method and testing, see if it can be improved. You don’t need to
do an optimal solution in the first attempt. Most of the time you can reduce the number
of lines and make an algorithm more elegant after an initial solution has been
provided.
