import mysql.connector as mysql
import os
from dotenv import load_dotenv
from mysql.connector import errorcode

load_dotenv()

DB_USER=os.getenv("DB_USER")
DB_PASSWORD= os.getenv("DB_PASSWORD")
DB_NAME="banking"
TABLES={}
TABLES['user']= ("""
        create table if not exists user (
        id int not null primary key auto_increment,
        fname varchar(30) not null,
        lname varchar(30) not null,
        street varchar(40) not null,
        city varchar(20) not null,
        post varchar(10) not null,
        phone varchar(12) not null,
        email varchar(320) not null,
        password varchar(72) not null)
        """
        )

TABLES['accounttype']=("""
        create table if not exists accounttype (
        id int not null primary key auto_increment,
        description varchar(20) not null)
        """)

TABLES['account']=("""
        create table if not exists account  (
        account_number int not null primary key auto_increment,
        account_type int not null,
        owner_id int not null,
        open_date date not null,
        status enum ('active', 'inactive') not null,
        balance decimal(15,2) default 0.00,

        constraint owner_id_fk foreign key(owner_id)
        references user(id)
        on update cascade on delete cascade,

        constraint account_type_fk foreign key(account_type)
        references accounttype(id)
        on update cascade on delete cascade)
        """)


TABLES['transactions']=("""
        create table if not exists transactions (
        id int not null primary key auto_increment,
        date date not null,
        account_number int not null,
        txn_type enum ('deposit', 'withdraw','transfer'),
        txn_amount decimal(10,2) not null,
        txn_description varchar(40) not null,

        constraint account_id_fk foreign key(account_number)
        references account(account_number)
        on update cascade on delete cascade
        )
        """)
connection=None

# Establishes database connection
def __connectToDb():
    try:
        global connection
        connection = mysql.connect(user=DB_USER, password=DB_PASSWORD, host='localhost') 
    except mysql.Error as err:
        if err.errno== errorcode.ER_ACCESS_DENIED_ERROR:
            print("Access denied. Incorrect credential")
        elif err.errno==errorcode.ER_BAD_DB_ERROR:
            print("Database doesn't exists")
        else:
            print(err)

# Use database DB_NAME, if the database doesn't exists
# it is created.
def __useDatabase():
    try:
        cursor=connection.cursor()
        cursor.execute("use {}".format(DB_NAME))
    except mysql.Error as err:
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            #database doesn't exist, so create it
            cursor.execute("create database {} default character set 'utf8'".format(DB_NAME))
            connection.database=DB_NAME
        else:
            print(err)
            connection.close()
            exit(1)

# Create all tables if they don't exists
def __createTables():
    cursor= connection.cursor()
    for table_name in TABLES: 
        try:
            cursor.execute(TABLES[table_name])
        except mysql.Error as err:
            print(err)
 
__connectToDb()
__useDatabase()
__createTables()


