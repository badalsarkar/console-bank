import datetime
from db import connection 
import mysql.connector as mysql


def createTransaction(transaction: dict, cursor=None):
    #validate data
    closeCursor = False
    if cursor == None:
        cursor = connection.cursor()
        closeCursor = True
    date = datetime.datetime.now() 
    newTransaction = (date, transaction["account_number"], transaction["txn_type"],
            transaction["txn_amount"], transaction["txn_description"])
    try:
        cursor.execute("""insert into transactions (date, account_number, txn_type, txn_amount,
                        txn_description) values(%s, %s, %s, %s, %s)""",newTransaction)
        if closeCursor:
            connection.commit()
            cursor.close()
    except mysql.Error as err:
        print (err)
        raise
    finally:
        if closeCursor:
            cursor.close()



def getAllTransactions(accountNumber: int)->[dict]:
    cursor = connection.cursor(dictionary= True)
    try:
        statement = f"select * from transactions where account_number = {accountNumber}"
        cursor.execute(statement)
        transactions = cursor.fetchall()
        return transactions
    except mysql.Error as err:
        print("Transactions can't be retrieved. Try again later")
        return None
    finally:
        cursor.close()
        

