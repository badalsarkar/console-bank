import pyinputplus as pyip
from db_user import UserDB
from getpass import getpass
import re
from utilities import getInputStr
from utilities import getNewPassword


FNAME_LENGTH=30
LNAME_LENGTH=30
STREET_LENGTH=40
CITY_LENGTH=20
POST_LENGTH=10
PHONE_LENGTH=12
EMAIL_LENGTH=320
PHONE_REGEX=r'\d{10}'
EMAIL_REGEX= r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
USER_VERIFIED=False
USER_ID=None


def signUp():
    """
    Creates an user.

    Takes user input from console, validates input and send to database.
    """
    #get the data
    fname= getInputStr(prompt="Enter your first name: ", maxlength=FNAME_LENGTH, regex=None)
    lname= getInputStr(prompt="Enter your last name: ", maxlength=LNAME_LENGTH, regex=None)
    street = getInputStr(prompt="Enter your street number and name: ", maxlength=STREET_LENGTH, regex=None)
    city = getInputStr(prompt="Which city do you live in? ", maxlength=CITY_LENGTH, regex=None)
    post = getInputStr(prompt= "What is your post code? ", maxlength=POST_LENGTH, regex=None) 
    phone = getInputStr(prompt="What is your phone number? ", maxlength=PHONE_LENGTH, regex=PHONE_REGEX)
    email = getInputStr(prompt="What is your email address? ", maxlength=EMAIL_LENGTH, regex=EMAIL_REGEX)
    password = getNewPassword() 

    #Send to database
    itemid=UserDB.createUser({
        "fname": fname,
        "lname": lname,
        "street": street,
        "city": city,
        "post": post,
        "phone": phone,
        "email": email,
        "password": password}
        )
    if itemid !=None:
        print("Account successfully created!")




def login():
    email=pyip.inputStr("Enter your email address: ")
    password= getpass("Enter your password: ")

    userId = UserDB.verifyUser(email, password)
    if userId != None: 
        global USER_VERIFIED
        USER_VERIFIED=True
        global USER_ID
        USER_ID= userId
        print("Successfully logged in")
    else:
        print("Login failed")



def logout():
    """
    User logout. 
    """
    global USER_VERIFIED
    USER_VERIFIED=False
    print("Successfully logged out")


