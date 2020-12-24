import pyinputplus as pyip
from getpass import getpass
import re
from rich.console import Console
from rich.table import Table


CONSOLE = Console()

# Get input and validate against length and regex
def getInputStr (prompt:str, maxlength:int=None, regex:list=None)-> str:
    def validateInput(text):
        if len(text) > maxlength:
            raise Exception(f"Max {maxlength} character is allowed")
        if regex !=None and re.match(regex,text) == None:
            raise Exception(f"Invalid input pattern")

    if maxlength != None or regex !=None:
        text = pyip.inputCustom(customValidationFunc=validateInput, prompt=prompt)
    else:
        text = pyip.inputStr(prompt=prompt)
    return text


# Get new password
def getNewPassword(regex="[a-zA-Z0-9!@#$%^&*]", minchar=6, maxchar=72):
    """
    Gets user input for new password.

    Currently, max 72 character are allowed.

    Parameters
    ----------
    regex: str
        Regular expression to match user input. This can 
        be specified to restrict the characters allowed for
        password.
    minchar: int
        Indicates minimum number of characters for password.
    maxchar: int
        Indicates maximum number of characters for password.
    """
    regex = regex+"{"+str(minchar)+","+str(maxchar)+"}"
    goodPassword = False
    password=None
    confirmPassword =None
    while not goodPassword:
        password = getpass("Enter new password: ") 
        if re.match(regex, password) == None:
            print(f"""Password not accepted.
            Accepted characters are {regex}.
            Minimum {minchar} and Maximum {maxchar} character needed""")
            continue
        confirmPassword = getpass("Confirm password: ") 
        if password != confirmPassword:
            print("Pass mismatch")
            continue
        else:
            goodPassword=True
    return password



def getMenuSelection(menu: dict)->int:
    """
    Gets user selection of menu item.

    It shows the menu, receives user's input,
    validates if the input is correct and return the
    input.

    Parameters
    ----------
    menu: dict
        The menu to be displayed.
    """
    validSelection= False
    selections= menu.keys()
    selection=None
    while not validSelection:
        __displayMenu(menu)
        try:
            selection = int(input("Enter your selection >> "))
            if selection not in selections:
                print("Invalid selection")
            else:
                validSelection=True
        except ValueError as err:
            print("Invalid selection")
    return selection




def getListSelection(items: list)->int:
    """
    Gets user selection of a list of items.

    It can be printed as ordered or unordered list
    """
    #TODO: return error if not list
    validSelection =False
    selection=None
    while not validSelection:
        __displayList(items)
        selection= int(input("Enter your selection >> "))
        if selection<1 and selection > len(items):
            CONSOLE.print("Invalid selection\n", style="bold red")
        else:
            validSelection=True
    return selection



def __displayMenu(menu):
    print("Select from below menu: ")
    for key in menu:
        print(menu[key])


def __displayList(items):
    print("Select from below options: ")
    i=1
    for item in items:
        print(f"[{i}] {item}")
        i+=1


def getInputAmount(prompt:str=None, minAmt:int=None, maxAmt:int=None, greaterThan: int = None, lessThan:int=None):
    """
    Gets user input for an amount.

    Amount can be with decimal point or without decimal point.
    """
    return pyip.inputNum(prompt=prompt, min=minAmt, max=maxAmt, greaterThan=greaterThan, lessThan=lessThan)


def getInputInt(prompt: str=None, acceptedValue: list=None):
    """
    Get an integer input from user. 

    If ``acceptedValue`` is given, it matches user input
    against it and prompts until a valid selection is made.
    """
    validSelection = False
    if validSelection != None:
        while not validSelection:
            try:
                selection = int(input(prompt))
                if selection in acceptedValue:
                    validSelection = True
                    break
            except ValueError as err:
                print("Invalid selection")
            else:
                print ("Invalid selection")
    return selection

    

def displayAsTable(data: dict, title: str="Sample Table",columnStyle: dict=None, rowStyle: dict=None):
    """

    The first row of the data must contain column names.

    Parameters
    ----------
    columnStyle: dict
        It is a dictionary where each item contains some
        styling information. The key is the table column name.
        It must match with column name. The value is another dictionary.

        style: dict
            This contains style information. The available options are-
            justify: (left, center, right, full)
            style: (color, bold)
            no_wrap: True/False


        
    """
    table = Table(title = title)
    columns = data[0].keys()
    for column in columns:
        if columnStyle != None:
            style = columnStyle[column]
            table = addTableColumnHeading(table, column, style)

    for item in data:
        row =[str (elem) for elem in list(item.values())] 
        table.add_row(*row)
    CONSOLE.print(table)


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
        table = addTableColumnHeading(table, column, columnStyle)

    # Add rows to table
    for account in accounts:
        # take each value and convert it to string and put it in the list
        row = [str (elem) for elem in list(account.values())]
        table.add_row(*row)
    CONSOLE.print(table)





def addTableColumnHeading(table: Table, columnName: str, columnStyle:dict={"justify":"left",
    "style":"cyan", "no_wrap":"True"}):
    """
    For a specific column of an account record, it creates
    a column object and attaches to the table.

    This allows to style each column separately and also dynamically
    adding column to the table.
    """
    table.add_column(columnName, justify=columnStyle["justify"], style=columnStyle["style"],
            no_wrap= columnStyle["no_wrap"])
    return table
