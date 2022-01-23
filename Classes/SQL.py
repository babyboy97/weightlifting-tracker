import mysql.connector
import pandas as pd

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

    def close_connection(self):
         self.my_database.close()

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