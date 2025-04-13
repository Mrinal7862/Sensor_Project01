import shutil
import os 
import sys 
from src.constant import * 
from src.utils.main_utils import MainUtils
from src.logger import logging
from src.exception import CustomException
from dataclasses import dataclass
import pickle
from flask import request
import pandas as pd 
import numpy as np
import train_pipe

@dataclass 
class PredictionPipelineConfig:
    """This class contains the configuration for the prediction pipeline."""

    prediction_output_dirname:str = 'predictions'
    prediction_file_name:str = "prediction_file.csv"
    model_file_path:str = os.path.join(artifact_folder, "model.pkl")
    preprocessor_path:str = os.path.join(artifact_folder, "preprocessor.pkl")
    prediction_file_path:str = os.path.join(prediction_output_dirname, prediction_file_name)


class PredictionPipeline:
    def __init__(self, request:request):

        self.request = request
        self.utils = MainUtils()
        self.prediction_pipeline_config = PredictionPipelineConfig()


    def save_input_files(self)->str:
        try:
            pred_file_input_dir = 'prediction_artifacts'
            os.makedirs(pred_file_input_dir, exist_ok=True)

            input_csv_file = self.request.files['file']

            pred_file_path = os.path.join(pred_file_input_dir, input_csv_file.filename)

            input_csv_file.save(pred_file_path)

            return pred_file_path
    
        except Exception as e:
            raise CustomException(sys, e)
        

    def predict(self, features):
        try:
            model = self.utils.load_object(self.prediction_pipeline_config.model_file_path)
            preprocessor =  self.utils.load_object(self.prediction_pipeline_config.preprocessor_path)


            transform_x = preprocessor.transform(features)

            predicts = model.predict(transform_x)


            return predicts
        
        except Exception as e:
            raise CustomException(sys, e)
        

    def get_predicted_dataframe(self, input_dataframe_path:pd.DataFrame):
        try:
            predict_column_name:str= TARGET_COLUMN
            input_dataframe:pd.DataFrame = pd.read_csv(input_dataframe_path)
            input_dataframe = input_dataframe.drop(columns="Unnamed: 0") if "Unnamed: 0" in input_dataframe.columns else input_dataframe

            predictions = self.predict(input_dataframe)

            input_dataframe[predict_column_name] = [pred for pred in predictions]

            target_column_mapping  = {0: "Bad", 1: "Good"}

            input_dataframe[predict_column_name] = input_dataframe[predict_column_name].map(target_column_mapping)

            os.makedirs(self.prediction_pipeline_config.prediction_output_dirname, exist_ok=True)

            input_dataframe.to_csv(self.prediction_pipeline_config.prediction_file_path, index=False)

            logging.info("Prediction Completed")

        except Exception as e:
            raise CustomException(sys, e)

    def run_pipeline(self):
        try:
            input_csv_path = self.save_input_files()
            get_predict = self.get_predicted_dataframe(input_csv_path)

            return self.prediction_pipeline_config
        except Exception as e:
            raise CustomException(sys, e)

