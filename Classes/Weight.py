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