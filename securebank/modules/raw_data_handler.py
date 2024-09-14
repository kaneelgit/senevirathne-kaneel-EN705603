import pandas
import json


class Raw_Data_Handler:

    def extract(self, customer_information_filename: str, transaction_filename: str, fraud_information_filename: str):
        """
        Inputs: The three data sources and convert them to pandas dataframes. 
        Returns: Three pandas dataframes made out of the three data sources
        """
        self.cif_df = self.open_file(customer_information_filename)
        self.tf_df = self.open_file(transaction_filename)
        self.fif_df = self.open_file(fraud_information_filename)

        #rename columns of fraud file
        new_cols = {0: 'trans_num', 1: 'is_fraud'}
        self.fif_df = self.fif_df.rename(columns = new_cols)
        
        return self.cif_df, self.tf_df, self.fif_df
    
    def transform(self, customer_information: pandas.DataFrame, transaction_information: pandas.DataFrame, fraud_information: pandas.DataFrame):
        """
        Function merges, standardizes and cleans columns and rows from the three data sources.
        """
        #first combine transaction details with fraud
        transactions_fraud = pandas.merge(transaction_information, fraud_information, on = 'trans_num')

        #then combine the customer file with the customer details using credit card number
        all_data = pandas.merge(transactions_fraud, customer_information, on = 'cc_num')

        #sort all data based on the transaction date and time.`trans_date_trans_time`.
        #convert transdate trans time to a time object. 
        all_data['trans_date_trans_time'] = pandas.to_datetime(all_data['trans_date_trans_time'])

        #drop index columns casue they aren't needed
        all_data = all_data.drop(columns = ['index_x', 'index_y'])

        #drop duplicates if any
        all_data = all_data.drop_duplicates()

        #drop is fraud nan rows. 
        raw_data = all_data[~all_data['is_fraud'].isna()]

        #sort by transdate and trans time
        self.raw_data = raw_data.sort_values(by='trans_date_trans_time')

        return self.raw_data 
    
    def describe(self, *args, **kwargs):
        
        version = kwargs.get('version', 'v1.0')
        storage_path = kwargs.get('storage', f'../data_sources/raw_data_{version}.parquet')
        
        #important columns 
        data_description = {}
        data_description['total samples'] = len(self.raw_data)
        data_description['fraud/no fraud split'] = f"{self.raw_data['is_fraud'].value_counts()[1]} / {self.raw_data['is_fraud'].value_counts()[0]}"

        result = {
            'version': version,
            'default storage': storage_path,
            'description': data_description
        }
        
        return result

    def load(self, raw_data: pandas.DataFrame, output_filename: str):
        """
        Saves the transformed data to a parquet file.
        """
        raw_data.to_parquet(output_filename, index=False)
        print(f"Raw data saved to {output_filename}")

    def open_file(self, filename):
        """
        Helper function to open the file and return a pandas dataframe. Currently accepting files, parquet, json and csv.
        """
        if filename.endswith('.csv'):
            return pandas.read_csv(filename)
        elif filename.endswith('.parquet'):
            return pandas.read_parquet(filename)
        elif filename.endswith('.json'):
            with open(filename, 'r') as file:
                data = json.load(file)
            return pandas.DataFrame(list(data.items()))
        else:
            raise ValueError("Only parquet files are allowed.")
