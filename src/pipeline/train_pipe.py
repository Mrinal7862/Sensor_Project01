import os 
import sys
from src.components.data_ingestion import DataIngestion 
from src.components.data_transformation import dataTransformation
from src.components.model_trainer import ModelTrainerClass
from src.utils.main_utils import MainUtils
from src.exception import CustomException
from dataclasses import dataclass
from src.logger import logging

class TrainingPipelineClass:
    def start_data_ingestion_method(self):
        try:
            data_ingestion = DataIngestion()
            feature_file_store = data_ingestion.initiate_data_ingestion()
            return feature_file_store
        except Exception as e:
            raise CustomException(e, sys)

    def start_data_transformation(self, feature_store_file_path):
        try:
            data_transformation = dataTransformation(feature_store_file_path=feature_store_file_path)
            train_array, test_array, preprocessor_path = data_transformation.initiate_data_transform()
            return train_array, test_array, preprocessor_path
        
        except Exception as e: 
            raise CustomException(e, sys)
        
    def start_model_training(self, train_array, test_array):
        try:
            model_trainer = ModelTrainerClass()
            model_score = ModelTrainerClass.initiate_model(train_array=train_array, test_array=test_array)

            return model_score
        except Exception as e:
            raise CustomException(sys, e)

    
    def run_pipeline(self):
        try:
            feature_store_file_path = self.start_data_ingestion_method()
            train_array,test_array, preprocessor = self.start_data_transformation(feature_store_file_path=feature_store_file_path)
            r2score = self.start_model_training(train_array, test_array)

            print("Training Completed : ", r2score)
        
        except Exception as e:
            raise CustomException(sys, e)