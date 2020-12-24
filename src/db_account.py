import datetime
import mysql.connector as mysql
from db import connection 
from db_transaction import createTransaction
"""
Module to interact with account table in database.
"""

def createAccount(account: dict):
    """
    """
    #TODO: validate data
    date = datetime.datetime.now() 
    status ='active'

    newAccount =(account["account_type"], account["owner_id"],date,status,account["balance"])
    #insert account data
    cursor=connection.cursor()
    cursor.execute("""insert into account (account_type, owner_id, open_date, status, balance)
                    values(%s, %s, %s, %s, %s)""", newAccount)
    accountNo= cursor.lastrowid
    connection.commit()
    cursor.close()
    return accountNo


def getAccounts(owner_id, column: str=None):
    """
    Fetch an account from account table.

    Parameters
    ----------
    owner_id: str
        Owner id.

    column: str (optional) (default= "*")
        The column name to be fetched. This is a ',' separated string.
        For example: "account_number, account_type, balance"

        If not provided all the columns are returned.
    """
    cursor = connection.cursor(dictionary=True)
    # replace "account_type" and "owner_id" for better readability
    if column == None:
        column = "account_number, account_type, owner_id, open_date, status, balance"
    join=""

    if "account_type" in column:
        column = column.replace("account_type", " t.description as account_type ")
        join = " inner join accounttype as t on account.account_type = t.id "
    if "owner_id" in column:
        column = column.replace("owner_id", " o.fname as owner_id ")
        join = join + "inner join user as o on o.id = account.owner_id " 

    statement = "select "+column+" from account "+join + f"where owner_id ={owner_id}" 
    cursor.execute(statement)
    accounts = cursor.fetchall()
    cursor.close()
    return accounts



def getAccountById(accountNumber, column: str="*"):
    """
    Fetch an account from account table by id.

    Parameters
    ----------
    accountNumber: int
        Account id.
    """
    cursor = connection.cursor(dictionary=True)
    if column == None:
        column = "account_number, account_type, owner_id, open_date, status, balance"
    join=""

    if "account_type" in column:
        column = column.replace("account_type", " t.description as account_type ")
        join = " inner join accounttype as t on account.account_type = t.id "
    if "owner_id" in column:
        column = column.replace("owner_id", " o.fname as owner_id ")
        join = join + "inner join user as o on o.id = account.owner_id " 

    statement = "select "+column+" from account "+join + f"where account_number ={accountNumber}" 
    cursor.execute(statement)
    account = cursor.fetchall()
    cursor.close()
    return account


def updateAccount(accountNumber: int, payload: str ):
    """
    Updates the columns with value.

    The columns to be updated and the value is passed as dictionary.

    Parameters
    ----------
    accountNumber: int
        The account to be updated
    payload: str
        a ',' seperated string where column and values are seperated by '='.
        For example, "balance=3000, status='inactive'"
    """
    statement = "update account set " + payload+ f" where account_number = {accountNumber}"
    cursor = connection.cursor()
    try:
        cursor.execute(statement)
        cursor.commit()
        cursor.close()
    except mysql.Error as err:
        print (err)
        raise
    else:
        cursor.close()


def depositToAccount(transaction: dict):
    cursor = connection.cursor()
    try:
        createTransaction(transaction, cursor)
        statement = f"""update account set balance = balance + {transaction["txn_amount"]} where account_number = {transaction["account_number"]}"""
        cursor.execute(statement)
        connection.commit()
        cursor.close()
    except mysql.Error as err:
        print (err)
        raise
    finally:
        cursor.close()

def withdrawFromAccount(transaction: dict)->None:
    cursor = connection.cursor()
    try:
        createTransaction(transaction, cursor)
        statement = f"""update account set balance = balance - {transaction["txn_amount"]} where account_number = {transaction["account_number"]}"""
        cursor.execute(statement)
        connection.commit()
        cursor.close()
    except mysql.Error as err:
        print (err)
        raise
    finally:
        cursor.close()
