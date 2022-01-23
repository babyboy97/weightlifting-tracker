from config import aws_endpoint, aws_master_username, aws_master_password, database
import mysql.connector
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

    def execute_sql(self, query:str):
        """Calls the initate function then passes the query to insert data

        Args:
            query (str): SQL query function

        Exception: Must pass str type for query variable
        """
        if not isinstance(query,str): 
            raise Exception("Must pass str for query")
                    
        self.my_cursor.execute(query)

        self.my_database.commit()


class Lifts(SQL): 
    def new_lift(self, lift:int, set_number:int, reps:int, weight:int, lift_date:str):
        """Provide ability to import into the lift table

        Args:
            set_number (int): Set Number
            reps (int): Reps performed
            weight (int): Weight lifted for each rep in the set
            lift_date (str): Date performed

        Exception: Must provide integar type for set_number, reps, weight, lift_date
        """
        
        if not all([isinstance(lift,int),isinstance(set_number,int),isinstance(reps,int),isinstance(weight,int)]):
            raise Exception("Please provide integar type for set_number, reps, weight, lift_date")

        query = f"""INSERT INTO WEIGHTLIFTING.LIFTS (LIFT,SET_NUMBER,REPS,WEIGHT,LIFT_DATE) 
                    VALUES ({lift},{set_number},{reps},{weight},'{lift_date}');"""

        SQL.execute_sql(self,query)

    
class Weight(SQL):
    """Provide ability to import body weight into the weight table

    Args:
        SQL ([type]): [description]
    """
    def new_weight(self, weight:int, weight_date:str):
        if not isinstance(weight,int): 
            raise Exception("Must provide integar type for weight")
        if not isinstance(weight_date,str):
            raise Exception("Must provide str type for weight_date")

        query = f"""INSERT INTO WEIGHTLIFTING.BODY_WEIGHT (WEIGHT, WEIGHT_DATE) 
                    VALUES ({weight},'{weight_date}');"""
        
        SQL.execute_sql(self,query)
        
