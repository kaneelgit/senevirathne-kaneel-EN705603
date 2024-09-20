import pandas
import sklearn
from datetime import datetime
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import json

class Feature_Extractor:

    def extract(self, training_dataset_filename: str, testing_dataset_filename: str):
        """
        This method inputs a raw train and test datasets in parquet format and output two pandas dataframes.
        If another file format is given it raises an error.
        """

        if training_dataset_filename.endswith('.parquet'):
            training_dataset =  pandas.read_parquet(training_dataset_filename)
        else:
            training_dataset = None

        if testing_dataset_filename.endswith('.parquet'):
            testing_dataset =  pandas.read_parquet(testing_dataset_filename)
        else:
            testing_dataset = None

        if (training_dataset is None) or (testing_dataset is None):
            raise ValueError("Only parquet files are allowed.")    
        else:
            return training_dataset, testing_dataset

    def transform(self, training_dataset: pandas.DataFrame, testing_dataset: pandas.DataFrame):

        #get unix diff
        # training_dataset['trans_diff'] = training_dataset['trans_date_trans_time'].diff().dt.total_seconds()
        # testing_dataset['trans_diff'] = testing_dataset['trans_date_trans_time'].diff().dt.total_seconds()
        training_dataset['trans_diff'] = training_dataset.groupby('cc_num')['trans_date_trans_time'].diff().dt.total_seconds()
        testing_dataset['trans_diff'] = testing_dataset.groupby('cc_num')['trans_date_trans_time'].diff().dt.total_seconds()
        
        #convert time to hour, day and year
        training_dataset = self.extract_hour_day_month(training_dataset)
        testing_dataset = self.extract_hour_day_month(testing_dataset)
        
        #create age column
        training_dataset = self.extract_age(training_dataset)
        testing_dataset = self.extract_age(testing_dataset)

        #combine categorical columns. Everything greater than a threshold will be changed to other
        training_dataset, testing_dataset = self.combine_categories(training_dataset, testing_dataset, 'state', 5000)
        training_dataset, testing_dataset = self.combine_categories(training_dataset, testing_dataset, 'job', 2000)
        training_dataset, testing_dataset = self.combine_categories(training_dataset, testing_dataset, 'city', 2000)
        training_dataset, testing_dataset = self.combine_categories(training_dataset, testing_dataset, 'zip', 2000)
        training_dataset, testing_dataset = self.combine_categories(training_dataset, testing_dataset, 'merchant', 2000)

        #convert categorical columns to ints
        column_mappings = {}
        training_dataset, testing_dataset, column_mappings['state'] = self.convert_categorical_to_integers(training_dataset, testing_dataset, 'state')
        training_dataset, testing_dataset, column_mappings['category'] = self.convert_categorical_to_integers(training_dataset, testing_dataset, 'category')
        training_dataset, testing_dataset, column_mappings['merchant'] = self.convert_categorical_to_integers(training_dataset, testing_dataset, 'merchant')
        training_dataset, testing_dataset, column_mappings['sex'] = self.convert_categorical_to_integers(training_dataset, testing_dataset, 'sex')
        training_dataset, testing_dataset, column_mappings['city'] = self.convert_categorical_to_integers(training_dataset, testing_dataset, 'city')
        training_dataset, testing_dataset, column_mappings['zip'] = self.convert_categorical_to_integers(training_dataset, testing_dataset, 'zip')
        training_dataset, testing_dataset, column_mappings['job'] = self.convert_categorical_to_integers(training_dataset, testing_dataset, 'job')
        training_dataset, testing_dataset, column_mappings['day_of_trans'] = self.convert_categorical_to_integers(training_dataset, testing_dataset, 'day_of_trans')
        training_dataset, testing_dataset, column_mappings['month_of_trans'] = self.convert_categorical_to_integers(training_dataset, testing_dataset, 'month_of_trans')
        
        #print highly correlated columns
        self.print_high_correlation_columns(training_dataset[['amt', 'lat', 'long', 'city_pop', 'merch_lat', 'merch_long']])

        #interested columns
        int_cols = ['trans_diff', 'day_of_trans', 'hour_of_trans', 'month_of_trans', 'age', 'state', 'merchant', 'category', 'sex', 'city', 'zip', 'job', 'amt', 'lat', 'long', 'city_pop', 'merch_lat', 'merch_long']
        target = 'is_fraud'
        
        #drop na values        
        training_dataset = training_dataset.dropna(subset = int_cols + [target])
        testing_dataset = testing_dataset.dropna(subset = int_cols + [target])

        #seperate training/testing featrues and target
        self.X_train = training_dataset[int_cols]
        self.y_train = training_dataset[target]

        self.X_test = testing_dataset[int_cols]
        self.y_test = testing_dataset[target]

        return [self.X_train, self.y_train, self.X_test, self.y_test], column_mappings

    def describe(self, *args, **kwargs):
        
        version = kwargs.get('version', 'v1.0')
        column_mapper = kwargs.get('column_mapper', None)
        column_mapper_path = kwargs.get('column_mapper_path', f'../data_sources/column_mapper_{version}.txt')

        if column_mapper is not None:
            with open(column_mapper_path, 'w') as f:
                json.dump(column_mapper, f)
            print(f"Column mapper saved in {column_mapper_path}")

        #important columns 
        data_description = {}
        data_description['X_train shape'] = self.X_train.shape
        data_description['y_train shape'] = self.y_train.shape
        data_description['X_test shape'] = self.X_test.shape
        data_description['y_test shape'] = self.y_test.shape
        data_description['Training Features'] = self.X_train.columns.to_list()

        result = {
            'version': version,
            'Column Mapper path': column_mapper_path,
            'description': data_description
        }
        
        return result
    
    def extract_hour_day_month(self, dataframe: pandas.DataFrame):
        """
        Helper function to convert columns to time, trans_date_trans_time to hour, day and month of the year.
        """
        dataframe['hour_of_trans'] = [x.hour for x in dataframe['trans_date_trans_time']]
        dataframe['day_of_trans'] = [x.day_name() for x in dataframe['trans_date_trans_time']]
        dataframe['month_of_trans'] = [x.month_name() for x in dataframe['trans_date_trans_time']]
        
        return dataframe
    
    def extract_age(self, dataframe: pandas.DataFrame):
        """
        Helper function to extract age from dob column
        """
        dataframe['dob'] = pandas.to_datetime(dataframe['dob'])
        dataframe['age'] = (datetime.now() - dataframe['dob']).astype('<m8[Y]')
        return dataframe

    def combine_categories(self, train_dataframe: pandas.DataFrame, test_dataframe: pandas.DataFrame, column: str, threshold: int):
        """
        Helper function to categorize data.
        """
        #  # Replace NaN values with 'Other' first
        # train_dataframe[column].fillna('Other', inplace=True)
        # test_dataframe[column].fillna('Other', inplace=True)
        
        mask = train_dataframe[column].value_counts() < threshold
        other_cats = mask[mask == True].index

        #change the category to other in the train and test dataframes
        train_dataframe[column] = ['Other' if x in other_cats else x for x in train_dataframe[column]]
        test_dataframe[column] = ['Other' if x in other_cats else x for x in test_dataframe[column]]
        
        return train_dataframe, test_dataframe

    def convert_categorical_to_integers(self, training_dataframe: pandas.DataFrame, testing_dataframe: pandas.DataFrame, column: str):
        """
        Convert a pandas categorical column to integers and return the mappings.
        """

        new_column = f"{column}"

        #create new column
        training_dataframe[new_column], uniques = pandas.factorize(training_dataframe[column], sort = True)
        # mappings_dict = {i: v for i, v in enumerate(uniques)}
        mappings_dict = {v:i for i, v in enumerate(uniques)}

        # Add 'Other' to the mappings if it's not already there
        if 'Other' not in mappings_dict:
            other_value = len(mappings_dict)  # Assign the next available integer for 'Other'
            mappings_dict['Other'] = other_value
        
        #change the mapping for testing set
        testing_dataframe[new_column] = testing_dataframe[column].map(mappings_dict)
        testing_dataframe[column].fillna(mappings_dict['Other'], inplace = True) #if not available make it other category

        return training_dataframe, testing_dataframe, mappings_dict

    def scale_column(self, training_dataset: pandas.DataFrame, testing_dataset: pandas.DataFrame, column: str):
        """
        Function to scale a column given trainign and testing data and column. Returns the scaled column.
        """
        scaler = MinMaxScaler()
        scaler.fit(training_dataset[[column]])

        #transform training values
        training_dataset[column] = scaler.transform(training_dataset[[column]])

        #use same scaler to transform testing datast values
        testing_dataset[column] = scaler.transform(testing_dataset[[column]])

        return training_dataset, testing_dataset
    
    def print_high_correlation_columns(self, df, threshold=0.9):
        # Compute the correlation matrix
        corr_matrix = df.corr().abs()
        
        # Create an upper triangle matrix to avoid duplicate comparisons
        upper_triangle = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
        
        # Find features with correlation above the threshold
        high_corr_columns = {}
        for column in upper_triangle.columns:
            correlated_features = upper_triangle.index[upper_triangle[column] > threshold]
            if len(correlated_features) > 1:
                high_corr_columns[column] = list(correlated_features)
        
        # Print columns with high correlations
        print("Columns with high correlations:")
        for col, corr_list in high_corr_columns.items():
            print(f"{col}: {', '.join(corr_list)}")
    
# fe = Feature_Extractor()

# data = fe.extract('../data_sources/train_data_v1.0.parquet', '../data_sources/test_data_v1.0.parquet')
# data_, cmp = fe.transform(data[0], data[1])

# import pdb; pdb.set_trace()