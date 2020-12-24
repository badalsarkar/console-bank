import pyinputplus as pyip
import db
import user
import account
import products
import transactions
from utilities import getMenuSelection
from menus import Menu
from menus import LoggedInMenu
from menus import MainMenu
from rich_config import console
from rich.panel import Panel
import os

# Controls when the program exits
exitProgram = False


# Attach a method to each menu item.
# Each menu item invokes a specific function.
# When user makes a selection, it is matched with
# this dictionary to invoke the related function
FUNCTION = {}
FUNCTION[Menu.SignUp.value] = user.signUp
FUNCTION[Menu.LogIn.value] = user.login
FUNCTION[Menu.ViewProducts.value] = products.showProducts
FUNCTION[Menu.Exit.value] = None
FUNCTION[Menu.CreateAccount.value] = account.createAccount
FUNCTION[Menu.ViewAccounts.value] = account.getAllAccounts
FUNCTION[Menu.DepositMoney.value] = account.deposit
FUNCTION[Menu.WithdrawMoney.value] = account.withdraw
FUNCTION[Menu.ViewTransactions.value] = transactions.viewTransactions
FUNCTION[Menu.LogOut.value] = user.logout


def run():
    showGreetings()
    # Program entry point
    while not exitProgram:
        if user.USER_VERIFIED:
            selection = getMenuSelection(LoggedInMenu)
            FUNCTION[selection]()
        else:
            selection = getMenuSelection(MainMenu)
            FUNCTION[selection]()


def showGreetings():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    console.print("WELCOME TO CONSOLE BANK",
                  style="bold white on blue", justify="center")
    console.print()
    console.print()
    console.print()


def exit():
    global exitProgram
    exitProgram = True
    console.print("Thank you for choosing Console Bank", style="bold green")


FUNCTION[Menu.Exit.value] = exit

# Run the program
run()
