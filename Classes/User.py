class User(SQL):
    def new_user(self, first_name:str, last_name:str, email:str, user_password:str, birthday:str):
        """Provides the ability to create a new user account.

        args: 
            first_name (str): First name of the user
            last_name (str): Last name of the user
            email (str): User's email 
            user_password (str): User's password
            birthday (str): User's birthday

        Exception: Must pass str for each variabled
        Exception: Must input a string for first name and last name
        Exception: Must create a password at least 8 character longs
        Exception: Must pass valid email
        Exception: Email address already in use. Please choose another.        
        """
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
            raise Exception("Please pass a valid email")

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

    def user_birthday_handling(date):
        try:
            dt_date = datetime.strptime(date, '%Y-%m-%d')
        except Exception as e:
            raise Exception("Please pass date in YYYY-MM-DD format.")

        if (dt_date.year < 1950) or (dt_date >= datetime.today()):
            raise Exception("Please enter a valid birthday.")