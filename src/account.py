import user
from enum import Enum
import db_account as AccountDB
from utilities import getMenuSelection
from utilities import getInputAmount
from utilities import getInputInt
from utilities import getInputStr
from rich.console import Console
from rich.table import Table
from user import USER_ID

ACCOUNTS ={1:"[1] Chequing", 2:"[2] Savings", 3:"[3] Investment"}
CONSOLE = Console()

class Account(Enum):
    account_number= "account_number"
    account_type= "account_type"
    owner_id= "owner_id"
    open_date= "open_date"
    balance= "balance"
    status= "status"



def createAccount():
    """
    Creates an account and save to database.

    Take user input, validate input, create an account and 
    store into the database.
    """
    account_type = int(getMenuSelection(ACCOUNTS)) 
    balance =getInputAmount("How much would like to deposit now? ") 
    owner_id = user.USER_ID

    accountNo = AccountDB.createAccount({"account_type":account_type, "balance":balance, "owner_id":owner_id})
    if accountNo != None:
        CONSOLE.print("Account successfully created", style="bold green")
        CONSOLE.print("Here is the details of your new account:")
        account = AccountDB.getAccountById(accountNo)
        displayAccountDetails(AccountDB.getAccountById(accountNo))




def getAllAccounts():
    """
    Gets all accounts from database and displays to console.

    """
    allAccounts = AccountDB.getAccounts(user.USER_ID)
    displayAccountDetails(allAccounts)




def deposit():
    """
    Takes an account and an amount. Increases the balance
    of the account by the amount.
    """
    selectedAccount = chooseAccount() 
    txnAmount = getInputAmount("Enter deposit amount: ", minAmt = 1)
    txnDescription = getInputStr("Enter transaction description: ")
    try:
        AccountDB.depositToAccount({"account_number": selectedAccount, "txn_type": "deposit",
            "txn_amount":txnAmount, "txn_description": txnDescription})
    except Exception as err:
        print (err)
        print ("Transaction did not complete")




def withdraw():
    """
    Takes an account and an amount. If the amount is less than
    or equal to the account balance, the balance is reduced by
    the amount.
    """
    selectedAccount= chooseAccount()
    currentBalance = float (AccountDB.getAccountById(selectedAccount, "balance")[0]["balance"])
    if currentBalance == 0:
        print("You have no money to withdraw.")
        return
    txnAmount= getInputAmount(prompt="Enter withdraw amount: ", minAmt = 1, maxAmt=currentBalance)
    txnDescription = getInputStr("Enter transaction description: ")
    try:
        AccountDB.withdrawFromAccount({"account_number": selectedAccount, "txn_type": "withdraw",
            "txn_amount":txnAmount, "txn_description": txnDescription})
        print("Withdrawal completed successfully.")
    except Exception as err:
        print (err)
        print("Transaction could not be completed. Try again later.")




def chooseAccount()->int:
    # Provides a list of accounts to choose from.
    # Returns the user selection.
    accounts = AccountDB.getAccounts(user.USER_ID, "account_number, account_type, owner_id, balance, status") 
    validSelection = []
    for account in accounts:
        validSelection.append(account["account_number"])
    print("You have the following accounts")
    displayAccountDetails(accounts)
    selectedAccount = getInputInt("Enter your selection :", validSelection)
    return selectedAccount





def displayAccountDetails(accounts: [dict])->None:
    """
    Displays account detail in a table.

    A row is a record of an account. It contains information like
    account_type, account_number, balance etc. These are the table
    column. ``accounts`` can contain multiple record.

    The table column and rows are created dynamically.

    Parameters
    accounts: [dict]
        A list of dictionary that contains information about multiple accounts.
    ---------
    """
    table = Table(title="Account details")
    # Get one record to extract the column names
    columns = accounts[0].keys()
    # Add all column heading to ``table``
    for column in columns:
        table = addTableColumnHeading(table, column)

    # Add rows to table
    for account in accounts:
        # take each value and convert it to string and put it in the list
        row = [str (elem) for elem in list(account.values())]
        table.add_row(*row)
    CONSOLE.print(table)





def addTableColumnHeading(table: Table, columnName: str):
    """
    For a specific column of an account record, it creates
    a column object and attaches to the table.

    This allows to style each column separately and also dynamically
    adding column to the table.
    """
    if Account(columnName) == Account.account_number:
        table.add_column(columnName, justify="left", style="cyan", no_wrap=True)

    if Account(columnName) == Account.account_type:
        table.add_column(columnName, justify="left", style="magenta", no_wrap=True)

    if Account(columnName) == Account.owner_id:
        table.add_column(Account.owner_id.value, justify="left", style="cyan", no_wrap=True)

    if Account(columnName) == Account.open_date:
        table.add_column(Account.open_date.value, justify="left", style="magenta", no_wrap=True)

    if Account(columnName) == Account.balance:
        table.add_column(Account.balance.value, justify="right", style="cyan", no_wrap=True)

    if Account(columnName) == Account.status:
        table.add_column(Account.status.value, justify="left", style="magenta", no_wrap=True)
    return table
