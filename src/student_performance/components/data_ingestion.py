import os
import sys
from src.student_performance.exception import CustomException
from src.student_performance.logger import logging
import pandas as pd
from src.student_performance.utils import read_sql_data

from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.student_performance.components.data_transformation import DataTransformation
from src.student_performance.components.data_transformation import DataTransformationConfig

from src.student_performance.components.model_trainer import ModelTrainerconfig
from src.student_performance.components.model_trainer import ModelTrainer


@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join("artifacts","train.csv")
    test_data_path: str = os.path.join("artifacts","test.csv")
    raw_data_path: str = os.path.join("artifacts","raw.csv")


class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):

        try:
            df = read_sql_data()
            logging.info("reading completed  from mysql database") 

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)

            logging.info("train test split initiated")
            train_set,test_set = train_test_split(df,test_size=0.2,random_state=30)

            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)

            logging.info("ingestion of data completed")

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path,
            )
        except Exception as e:
            raise CustomException(e,sys)


if __name__=="__main__":
    obj=DataIngestion()
    train_data,test_data=obj.initiate_data_ingestion()

    data_transformation=DataTransformation()
    train_arr,test_arr,_=data_transformation.initiate_data_transformation(train_data,test_data)
    try:

        modeltrainer=ModelTrainer()
        print(modeltrainer.initiate_model_trainer(train_arr,test_arr))

    except Exception as e:
        raise CustomException(e,sys)