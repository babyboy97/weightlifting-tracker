from config import aws_endpoint, aws_master_username, aws_master_password, database
from datetime import datetime
import pandas as pd

# Classes
from Classes.User import User
from Classes.Weight import Weight
from Classes.Lifts import Lifts


# # Create user 

# U = User(aws_endpoint, aws_master_username, aws_master_password, database)
# U.new_user('Chris', 'Chaplin', 'aemail@gmail.com', 'qwertyuiop', '1995-01-01')
# U.close_connection()

# W = Weight(aws_endpoint, aws_master_username, aws_master_password, database)
# W.new_weight(35, 130.5, '2022-01-23')
# W.close_connection()

# L = Lifts(aws_endpoint, aws_master_username, aws_master_password, database)
# L.new_lift(123, 5, 9, 10, 100, '2022-01-23')
# L.close_connection()
