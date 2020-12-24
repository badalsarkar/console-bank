from db import connection 
import bcrypt

class UserDB:
    """ Provides functionality to interact with user table"""

    @staticmethod
    def createUser(user:dict):
        """ Add a record in the user table 

        Parameters
        ----------
        user: tuple
            The user data. It must have the following items-
                fname: str
                    The first name of user
                lname: str
                    The last name of user
                street: str
                    The street number and name
                city: str
                    The city name
                post: str
                    The post code
                phone: str
                    User's phone number
                email: str
                    User's email address
        """
        #Validate user data
        # TODO: validation 

        #hash password
        user["password"]= UserDB.__encryptPassword(user["password"])
        user=(user["fname"],user["lname"], user["street"], user["city"], user["post"],
                user["phone"], user["email"], user["password"])

        #insert user data
        cursor=connection.cursor()
        cursor.execute("""insert into user (fname, lname, street, city, post, phone, email, password)
                        values(%s, %s, %s, %s, %s, %s, %s, %s)""", user)
        userNo= cursor.lastrowid
        connection.commit()
        cursor.close()
        return userNo
    


    @staticmethod
    def getFromUser(email:str, column:str):
        """
        Fetch some columns from user table.

        Column names are given as ',' separated string.
        Example: city, post

        Parameters
        ----------
        email:str
            User's email address
        column:str
            Desired column name separated by ','

        Returns
        -------
        records: list
            A list of rows
        """
        cursor= connection.cursor()
        statement= f"select {column} from user where email='{email}'"
        cursor.execute(statement)
        records = cursor.fetchall()
        cursor.close()
        return records



    def verifyUser(email:str, password:str):
        """
        Retrieves user's password and match against given password.

        Parameters
        ----------
        email: str
            User's email address
        password: str
            User's password

        Returns
        -------
        True if password matches.
        """
        user = UserDB.getFromUser(email, 'password, id')
        if len(user) == 0:
            return None
        else:
            if bcrypt.checkpw(password.encode(), user[0][0].encode()):
                return user[0][1] 
            else:
                return None



    def deleteUser():
        pass

    def updateUser():
        pass



    @staticmethod
    def __encryptPassword(password:str)->str:
        encrypted = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        return encrypted


    @staticmethod
    def __decryptPassword(password:str, encryptedPass:str)->str:
        return bcrypt.checkpw(password, encryptedPass)

