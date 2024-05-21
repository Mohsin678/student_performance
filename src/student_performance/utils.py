import os
import sys
from src.student_performance.exception import CustomException
from src.student_performance.logger import logging
import pandas as pd
from dotenv import load_dotenv
import pymysql

load_dotenv()

host =os.getenv("host")
user = os.getenv("user")
password = os.getenv("password")
db = os.getenv("db")

def read_sql_data():
    logging.info("reading sql base started")
    try:
        mydb = pymysql.connect(
            host = host,
            user=user,
            password=password,
            db=db
        )
        logging.info("connection established",mydb)
        df = pd.read_sql_query("select * from students",mydb)
        return df

    except Exception as e:
        raise CustomException(e)

