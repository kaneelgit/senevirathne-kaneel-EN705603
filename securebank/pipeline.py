import os
import argparse 
import pandas as pd
import ast
from datetime import datetime
import joblib
from modules import raw_data_handler

class Pipeline:

    def __init__(self, model_version: str = "logistic_regression_v1", column_mapper_version: str = "v1"):

        #initialize model version
        self.model_version = model_version
        model_dir = f"storage/models/artifacts/{self.model_version}.pkl"
        self.column_mapper_dir = f"data_sources/column_mapper_{column_mapper_version}.0.txt"

        with open(self.column_mapper_dir, 'r') as file:
            self.column_mapper = file.read()
        #convert mapper to a dict
        self.column_mapper = ast.literal_eval(self.column_mapper)

        #load model
        self.select_model(model_dir)

    def predict(self, input_data):
        
        #select get data from cc 
        inference_df = self.card_holder_info(input_data)
        #load model and make prediction 
        prediction = self.model.predict(inference_df)
        model_predict = 'Transaction Declined: Fraud Detected.' if prediction == 1 else 'Transaction Approved.'

        #save data in a dataframe for history

        return f"{model_predict}\nModel: {self.model_version}\n"

    def select_model(self, model_dir):
        """
        loads a model from a catalog of pre-trained models in storage/models/artifacts/
        """
        self.model = joblib.load(model_dir)

    def get_history(self):
        """
        Model results
        """
        #print history dataframe
        history_df = pd.read_csv("storage/models/model_history.csv")
        return history_df
    
    def card_holder_info(self, input_dict, customer_information = 'data_sources/customer_release.csv', transaction_information = "data_sources/transactions_release.parquet", fraud_information = "data_sources/fraud_release.json"):
        
        #get credit card number and get information for the client
        cc_num = int(input_dict['cc_num'])

        #use raw data handler to get customer information and transaction information to get customers last transaction time
        rdh = raw_data_handler.Raw_Data_Handler()
        cr, ti, _ = rdh.extract(customer_information, transaction_information, fraud_information)
        
        #sort by time
        ti = ti.sort_values(by='trans_date_trans_time')
        #get customer last transaction time
        ti_patient = ti[ti['cc_num'] == cc_num]
        lt = ti_patient['trans_date_trans_time'].iloc[-1]

        #get patient info
        # cr = pd.read_csv(data_source)
        cr_patient = cr[cr['cc_num'] == cc_num]
        cr_patient['dob'] = pd.to_datetime(cr_patient['dob'])

        #get data from cc num
        trans_date_trans_time = datetime.strptime(input_dict['trans_date_trans_time'], '%Y-%m-%d %H:%M:%S')
        trans_date_trans_time = pd.to_datetime(trans_date_trans_time)

        #store data in a dictionary and convert data to the training set formats
        new_data_dict = {}

        #transaction time difference
        new_data_dict['trans_diff'] = (trans_date_trans_time - pd.to_datetime(lt)).total_seconds()     
        new_data_dict['day_of_trans'] = self.column_mapper['day_of_trans'][trans_date_trans_time.day_name()]
        new_data_dict['hour_of_trans'] = trans_date_trans_time.hour
        new_data_dict['month_of_trans'] = self.column_mapper['month_of_trans'][trans_date_trans_time.month_name()]
        # new_data_dict['age'] = (datetime.now() - cr_patient['dob']).astype('<m8[Y]')
        new_data_dict['age'] = (pd.Timestamp.now() - cr_patient['dob']).astype('timedelta64[Y]')
        
        new_data_dict['state'] = self.column_mapper['state'][cr_patient['state'].iloc[0]]

        if input_dict['merchant'] not in self.column_mapper['merchant']:
            merch = "Other"
        else:
            merch = input_dict["merchant"]

        new_data_dict['merchant'] = self.column_mapper['merchant'][merch]

        if input_dict['category'] not in self.column_mapper['category']:
            cat = "Other"
        else:
            cat = input_dict['category']
            
        new_data_dict['category'] = self.column_mapper['category'][cat]
        new_data_dict['sex'] = self.column_mapper['sex'][cr_patient['sex'].iloc[0]]

        if cr_patient['city'].iloc[0] not in self.column_mapper['city']:
            city = "Other"
        else:
            city = cr_patient['city'].iloc[0]

        new_data_dict['city'] = self.column_mapper['city'][city]

        if cr_patient['zip'].iloc[0] not in self.column_mapper['zip']:
            zip = "Other"
        else:
            zip = cr_patient['zip'].iloc[0]

        new_data_dict['zip'] = self.column_mapper['zip'][zip]

        if cr_patient['job'].iloc[0] not in self.column_mapper['job']:
            job = "Other"
        else:
            job = cr_patient['job'].iloc[0]

        new_data_dict['job'] = self.column_mapper['job'][job]
        
        new_data_dict['amt'] = input_dict['amt']
        new_data_dict['lat'] = cr_patient['lat'].iloc[0]
        new_data_dict['long'] = cr_patient['long'].iloc[0]
        new_data_dict['city_pop'] = cr_patient['city_pop'].iloc[0]
        new_data_dict['merch_lat'] = input_dict['merch_lat']
        new_data_dict['merch_long'] = input_dict['merch_long']

        # int_cols = ['day_of_trans', 'hour_of_trans', 'month_of_trans', 'age', 'state', 'merchant', 'category', 'sex', 'city', 'zip', 'job', 'amt', 'lat', 'long', 'city_pop', 'merch_lat', 'merch_long']

        inference_df = pd.DataFrame(new_data_dict)

        return inference_df
    