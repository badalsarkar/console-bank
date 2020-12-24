from enum import Enum
import user

class Menu(Enum):
    # Holds a list of all menus.
    # The value of each item corresponds to the
    # number displayed to user. For example, SignUp is 
    # shown as 1. Create Account
    SignUp= 1 
    LogIn= 2 
    ViewProducts= 3 
    Exit = 4 
    CreateAccount=5
    ViewAccounts=6
    DepositMoney=7
    WithdrawMoney = 8
    ViewTransactions = 9
    LogOut = 10


# Creating main menu.
MainMenu={}
MainMenu[Menu.SignUp.value]= "1. Sign Up"
MainMenu[Menu.LogIn.value] = "2. Log in"
MainMenu[Menu.ViewProducts.value] ="3. View Products"
MainMenu[Menu.Exit.value] = "4. Exit"


# Creating Logged in menu
LoggedInMenu ={}
LoggedInMenu[Menu.CreateAccount.value]= "5. Create Account"
LoggedInMenu[Menu.ViewAccounts.value]= "6. View Accounts"
LoggedInMenu[Menu.DepositMoney.value] = "7. Deposit Money"
LoggedInMenu[Menu.WithdrawMoney.value] = "8. Withdraw Money"
LoggedInMenu[Menu.ViewTransactions.value] = "9. View Transactions"
LoggedInMenu[Menu.LogOut.value] = "10. Log Out"

