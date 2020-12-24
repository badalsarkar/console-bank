from account import chooseAccount  
from utilities import displayAsTable
import db_transaction as TransactionDB

def viewTransactions()->None:
    selectedAccount = chooseAccount()
    transactions = TransactionDB.getAllTransactions(selectedAccount) 
    displayAsTable(data= transactions, title="Transaction Details" ) 


