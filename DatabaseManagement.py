from config import aws_endpoint, aws_master_username, aws_master_password, database
import mysql.connector
import pandas as pd
from datetime import datetime
from email_validator import validate_email

class SQL:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.my_database = mysql.connector.connect(
                            host=self.host,
                            user=self.user,
                            password=self.password,
                            database=self.database
                        )
        # self.cursor = self.my_database.cursor()

    def query_data(self, query:str):
        """Provides the ability to query data from the database

        Args:
            query (str): SQL query

        Raises:
            Exception: Must pass str for query
            e: SQL syntax based error

        Returns:
            df (pd.DataFrame): Dataframe
        """
        cursor = self.my_database.cursor()

        if not isinstance(query,str): 
            raise Exception("Must pass str for query")
        
        try:
            cursor.execute(query)
            columns = cursor.description
            data = [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
            df = pd.DataFrame(data)
            cursor.close()
            return df
        except Exception as e:
            cursor.close()
            raise e
        
    def insert_data(self, query:str):
        """Calls the initate function then passes the query to insert data

        Args:
            query (str): SQL query function

        Exception: Must pass str type for query variable 
        """
        if not isinstance(query,str): 
            raise Exception("Must pass str for query")
        
        cursor = self.my_database.cursor()          
        
        try:
            pass
            cursor.execute(query)
            self.my_database.commit()
        except Exception as e:
            raise e
        
        cursor.close() 


class Lifts(SQL): 
    def new_lift(self, user_id:int, lift:int, set_number:int, reps:int, weight:int, lift_date:str):
        """Provide ability to import into the lift database

        Args:
            set_number (int): Set Number
            reps (int): Reps performed
            weight (int): Weight lifted for each rep in the set
            lift_date (str): Date performed

        Exception: Must pass int for user_id
        Exception: Must provide integar type for set_number, reps, weight, lift_date
        """
        if not isinstance(user_id, int): 
            raise Exception("Must pass int for user_id")
        if not all([isinstance(lift,int),isinstance(set_number,int),isinstance(reps,int),isinstance(weight,int)]):
            raise Exception("Please provide integar type for set_number, reps, weight, lift_date")

        query = f"""INSERT INTO WEIGHTLIFTING.LIFTS (USER_ID,LIFT,SET_NUMBER,REPS,WEIGHT,LIFT_DATE) 
                    VALUES ({user_id}, {lift},{set_number},{reps},{weight},'{lift_date}');"""

        SQL.insert_data(self,query)

    
class Weight(SQL):
    def new_weight(self, user_id:int, weight:float, weight_date:str):
        try: 
            weight = round(float(weight), 2)
        except Exception:
            raise Exception("Must provide float type for weight")

        if not isinstance(weight_date,str):
            raise Exception("Must provide str type for weight_date")

        query = f"""INSERT INTO WEIGHTLIFTING.BODY_WEIGHT (USER_ID, WEIGHT, WEIGHT_DATE) 
                    VALUES ({user_id}, {weight},'{weight_date}');"""
        
        SQL.insert_data(self,query)

class User(SQL):
    def new_user(self, first_name:str, last_name:str, email:str, user_password:str, birthday:str):


        if not all([isinstance(first_name, str), isinstance(last_name, str), isinstance(email, str), isinstance(user_password, str),isinstance(birthday, str)]):
            raise Exception("Please pass str for each variable")

        if not all([len(first_name) > 0, len(last_name) > 0]):
            raise Exception("Please input a string for first name and last name")

        if len(user_password) < 8:
            raise Exception("Please create a password at least 8 character longs") 

        # Email handling
        # Validate real email
        try: 
            validate_email(email)
        except Exception:
            raise Exception("Invalid email")

        # Dupe Email handling
        dupe_query = f"""SELECT * 
                        FROM WEIGHTLIFTING.USERS U 
                        WHERE LOWER(U.EMAIL) LIKE LOWER('{email.strip()}')"""
        output_df = SQL.query_data(self, dupe_query)
        
        if len(output_df) > 0:
            raise Exception("Email address already in use. Please choose another.")        

        # Birthday handling
        User.user_birthday_handling(birthday)

        # Creating User
        query = f"""INSERT INTO WEIGHTLIFTING.USERS (FIRST_NAME,LAST_NAME,EMAIL,USER_PASSWORD, BIRTHDAY) 
                    VALUES ('{first_name.strip()}', '{last_name.strip()}', '{email.strip()}', '{user_password}', '{birthday}');"""

        SQL.insert_data(self,query)

    def user_birthday_handling(date:str):
        """Handles birthday ensuring it is greater than 1950 and before today's date.

        Args:
            date (str): Birthday

        Raises:
            Exception: Must pass date in YYYY-MM-DD format.
            Exception: Must enter a valid birthday.
        """
        try:
            dt_date = datetime.strptime(date, '%Y-%m-%d')
        except Exception as e:
            raise Exception("Please pass date in YYYY-MM-DD format.")

        if (dt_date.year < 1950) or (dt_date >= datetime.today()):
            raise Exception("Please enter a valid birthday.")
        
