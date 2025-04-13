import sys
import os 
import numpy as np 
import pandas as pd 
from pymongo import MongoClient
from zipfile import Path
from src.constant import *
from src.exception import CustomException 
from src.utils.main_utils import MainUtils
from dataclasses import dataclass
import logging


@dataclass
class DataIngestionConfig:
    artifact_folder: str = os.path.join(artifact_folder)


class DataIngestion:
    def __init__(self):
        self.DataIngestionConfig = DataIngestionConfig()
        self.utils = MainUtils()
    
    def export_collection_as_dataframe(self, collection_name, db_name):

        try:
            mongo_client = MongoClient(MONGO_DB_URI)
            collection = mongo_client[db_name][collection_name]
            
            df = pd.DataFrame(list(collection.find()))

            if "_id" in df.columns.to_list:
                df = df.drop(columns=['_id'], axis=1)

            df.replace({"na": np.nan}, inplace=True)

            return df
        
        except Exception as e:
            raise CustomException(e, sys)
    
    def export_data_into_feature_store_file_path(self) -> pd.DataFrame:

        try:
            logging.info(f"Exporting data from MongoDB ")

            raw_file_path = self.DataIngestionConfig.artifact_folder

            os.makedirs(raw_file_path, exist_ok=True)

            sensor_data = self.export_collection_as_dataframe(
                collection_name=MONGO_COLLECTION_NAME,
                db_name=MONGO_DATABASE_NAME
            )

            logging.info(f"Saving Exported data into feature store file path: {raw_file_path}")

            feature_store_file_path = os.path.join(raw_file_path, "wafer_fault.csv")

            sensor_data.to_csv(feature_store_file_path, index=False)

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_ingestion(self) -> Path:
        try:
            logging.info(f"The data ingestion is of data integration class....")
            
            feature_store_file_path = self.export_data_into_feature_store_file_path()

            logging.info(f"Got the data from mongoDB")
            logging.info("Exited initiate_data_ingestion method of ingestion class")

            return feature_store_file_path
             
        except Exception as e:
            raise CustomException(e, sys) from e
    
