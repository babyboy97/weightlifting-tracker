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