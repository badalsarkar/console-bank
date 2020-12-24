from account import chooseAccount  
from utilities import displayAsTable
import db_transaction as TransactionDB
from rich_config import console

def viewTransactions()->None:
    selectedAccount = chooseAccount()
    transactions = TransactionDB.getAllTransactions(selectedAccount) 
    if transactions:
        displayAsTable(data= transactions, title="Transaction Details" ) 
    else:
        console.print("There is no transaction in this account", style="danger")




