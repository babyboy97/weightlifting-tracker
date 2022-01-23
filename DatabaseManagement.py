from config import aws_endpoint, aws_master_username, aws_master_password, database
import mysql.connector
import pandas as pd
from datetime import datetime


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
    def new_user(self, first_name:str, last_name:str, email:str, user_password:str):
        if not all([isinstance(first_name, str), isinstance(last_name, str), isinstance(email, str), isinstance(user_password, str)]):
            raise Exception("Please pass str for each variable")

        # Dupe Email check
        if len(W.query_data(f"""SELECT * FROM WEIGHTLIFTING.USERS U WHERE LOWER(U.EMAIL) LIKE LOWER('{email}')""")) > 0:
            raise Exception("Email address already in use. Please choose another.")        

        query = f"""INSERT INTO WEIGHTLIFTING.USERS (FIRST_NAME,LAST_NAME,EMAIL,USER_PASSWORD) 
                    VALUES ('{first_name.strip()}', '{last_name.strip()}', '{email}', '{user_password}');"""

        SQL.insert_data(self,query)
        
