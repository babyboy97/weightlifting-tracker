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
        self.my_cursor = self.my_database.cursor()

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
        if not isinstance(query,str): 
            raise Exception("Must pass str for query")
        
        try:
            self.my_cursor.execute(query)
            columns = self.my_cursor.description
            data = [{columns[index][0]:column for index, column in enumerate(value)} for value in self.my_cursor.fetchall()]
            df = pd.DataFrame(data)
            return df
        except Exception as e:
            raise e
        
    def insert_date(self, query:str):
        """Calls the initate function then passes the query to insert data

        Args:
            query (str): SQL query function

        Exception: Must pass str type for query variable
        """
        if not isinstance(query,str): 
            raise Exception("Must pass str for query")
                    
        try:
            self.my_cursor.execute(query)
            self.my_database.commit()
        except Exception as e:
            raise e


class Lifts(SQL): 
    def new_lift(self, lift:int, set_number:int, reps:int, weight:int, lift_date:str):
        """Provide ability to import into the lift database

        Args:
            set_number (int): Set Number
            reps (int): Reps performed
            weight (int): Weight lifted for each rep in the set
            lift_date (str): Date performed

        Exception: Must provide integar type for set_number, reps, weight, lift_date
        """
        
        if not all([isinstance(lift,int),isinstance(set_number,int),isinstance(reps,int),isinstance(weight,int)]):
            raise Exception("Please provide integar type for set_number, reps, weight, lift_date")

        query = f"""INSERT INTO WEIGHTLIFTING.LIFTS (LIFT,SET_NUMBER,REPS,BODY_WEIGHT,LIFT_DATE) 
                    VALUES ({lift},{set_number},{reps},{weight},'{lift_date}');"""

        SQL.insert_data(self,query)

    
class Weight(SQL):
    def new_weight(self, weight:int, weight_date:str):
        if not isinstance(weight,int): 
            raise Exception("Must provide integar type for weight")
        if not isinstance(weight_date,str):
            raise Exception("Must provide str type for weight_date")

        query = f"""INSERT INTO WEIGHTLIFTING.WEIGHT (WEIGHT, WEIGHT_DATE) 
                    VALUES ({weight},'{weight_date}');"""
        
        SQL.insert_data(self,query)
        
