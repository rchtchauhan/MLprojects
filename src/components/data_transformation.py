import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from src.exception import CustomException
from src.logger import logging
import os
import sys
from dataclasses import dataclass
from src.utils import save_object


@dataclass
class DataTrasformationConfig:
    preprocessor_obj_file_path = os.path.join("artifacts","preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTrasformationConfig()

    def get_data_transformation_object(self):
        try: 
            numerical_column=  ['writing_score', 'reading_score']
            categorical_column = ['gender', 'race_ethnicity', 'parental_level_of_education', 'lunch', 'test_preparation_course']

            num_pipleline = Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="median")),
                    ("scalar",StandardScaler())
                ]
            )

            # cat_pipleline = Pipeline(
            #     steps=[
            #         ("imputer",SimpleImputer(strategy="most_frequent")),
            #         ("scalar",StandardScaler()),
            #         ("one_hot_encoder",OneHotEncoder()),
            #         ("scalar",StandardScaler())
            #     ]
            # )
            cat_pipleline = Pipeline(
               steps=[
                ("imputer",SimpleImputer(strategy="most_frequent")),
                 ("one_hot_encoder",OneHotEncoder()),
                    ("scaler",StandardScaler(with_mean=False))
                            ]
                    )
            logging.info("Numerical column standard scalling done")
            logging.info("categorical column one hot coding done")

            preprossor = ColumnTransformer(
                [
                    ("num_pipeline",num_pipleline,numerical_column),
                    ("cat_pipeline",cat_pipleline,categorical_column)
                ]
            )

            return preprossor
            

        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self, train_path,test_path):
        try:

            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Reading train and Test data compelte")
            logging.info("obtaining preposses data ")

            preprosessing_obj = self.get_data_transformation_object()

            target_column_name = 'math_score'
            numerical_columns =  ['reading_score', 'writing_score']

            input_feature_train_df = train_df.drop(columns=[target_column_name],axis = 1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=[target_column_name],axis = 1)
            target_feature_test_df = test_df[target_column_name]


            logging.info(
                f"Applying preprocessing object on training dataframe and testing dataframe."
            )

            input_feature_train_arr = preprosessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprosessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info(f"saving preprossesing object")

            save_object(
                file_path = self.data_transformation_config.preprocessor_obj_file_path,
                obj = preprosessing_obj

            )
            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )



        except Exception as e:
            raise CustomException(e,sys)
    
            
