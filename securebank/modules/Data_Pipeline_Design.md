# Data Pipeline Design #

**Module to handle raw data and convert them into one data source: raw_data_hanlder.py**

This file is used to get all three datasets and combine it into one dataset in the parquet format. Here I have created a Raw_Data_Handler class with four functions extract, transform, load, describe and one helper function open_file to handle the data. 

The extract function inputs all three files and uses the open_file method to load the data. The open file method was used to identify the extension of the input string file string and then use it to load a csv, json file and a parquet format file accordingly. This functions convert all three datasets into pandas dataframes and returns them for further processing. 

Once extracted, files are loaded to the transform method to merge the dataset and convert them into a single file for further transformation. First we merge the transaction information dataframe and the fraud information dataframe using the transaction number ('trans_num') column. This was chosen because this was the unique transaction id and was the easiest method to combine these two datasets. Then this combined dataset is combined with the customer information. This was done using the common column credit card number ('cc_num'). 

Once merged a raw dataframe was created by getting rid of the rows that contained none values for the 'is_fraud' column. Since this is the target, rows containing none values would not be useful. So they were deleted. None values for the other columns were left in this stage since we can use imputation techniques or other methods to fill those none values if possible in later feature engineering steps. 

Once we have the raw dataset, the describe function was created to output the version, storage dir and a data description. I chose to have the length of the raw dataset and the number of fraud vs no fraud value counts as descriptions for the raw dataset. Since this is the raw dataset that is being used for other machine learning tasks, the size of the dataset and the distribution of the target value would be two important metrics to see in the raw dataset. Further descriptions will be performed in the feature engineering process. 

Below is an example of code usage. 
```
##file locations
ci, ti, fi = '../data_sources/customer_release.csv', '../data_sources/transactions_release.parquet', '../data_sources/fraud_release.json'

#initialize data handler
dh = Raw_Data_Handler()

#extract dataframes
df1, df2, df3 = dh.extract(ci, ti, fi)

#transform data
raw_data = dh.transform(df1, df2, df3)

#get a description of the dataset
desc = dh.describe()

#save the dataset in the desired directory.
dh.load(raw_data, desc['data_storage'])
```

**Module to design training and testing datasets: dataset_design.py**

In the second module, a similar class with four methods were created. The first method 'extract was used to import the dataset in parquet format. If any other data source was imported, the method raised an error. Once data is loaded a second method was implemented to seperate the dataset into train and test split. A default value of 0.2 was used as the test split. A default value of 42 was used for the random state. This could be changed if new datasets are created later in the machine learning training process.

In the describe class, the test and train data storage locations and the verison of the data was used as arguments. The version and the data storage was combined in order to be able to creagte a unique data source each time this function is used. The data description included the number of training and testing data samples and a descriptive statistic of the amount of fraud and non-fraud data samples in each train and test dataframes. This was done to make sure that the train test split is done properly before loading data to data storage. 

An example usage of the file is below. 

```
#raw data source
raw_dir = '../data_sources/raw_data_v1.0.parquet'

#initialize data desiner class
dd = Dataset_designer()

#extract the raw dataframe
raw_df = dd.extract(raw_dir)

#get the train test datasets using the sample function
data_list = dd.sample(raw_df)

#data description
result = dd.describe()

#save data
dd.load(data_list, result['Train default storage'], result['Test default storage'])

```

**Module to prepare dataset to machine learning training and testing: feature_extractor.py**

This module is used to create the training and testing sets for training and testing machine learning models. The parquet datasets are loaded and converted to pandas dataframes. Then they are transformed using different feature engineering methods for machine learning training. 

1. Hour, day and month.

Hour, day and month data from the 'trans_date_trans_time' columnn were extracted first because the initial analysis showed that the day, month and hour were associated with fraud transactions. A helper function was created and was used in the transform method to extract these data. This was done both for the training and testing datsets.

2. Age.

Next age was extracted from all the card holders. This was done using the 'dob' information provided.

3. Combining categorical data to 'Other'.

In order to make sure different categorical features were balanced, a new function combine_categories was created. This function took the 'column name' and the threshold to create the 'other' category. This then took all the categories < the threshold and binned them into one category 'Other'. This was perfomred on columns 'state', 'job', 'city', 'zip', 'merchant' with different suitable thresholds to match the data distribution. 

This was first perfomred to the training set and then the corresponding categories that qualified for the 'Other' category was changed in the testing set. The testing set was not used to determine the categories that would fall into the 'other' category.

4. Converting all categorical data to integers. 

Next all the categorical data were converted to integers for machine learning training. All datasets were converted into integers based on the number of categories in each feature. A column mapping for each feature was created and used to convert the testing dataset to the same categories for machine learning testing. Next these column mapper was saved in a dictionary format for future analaysis. (I.E to map from integer to real category to interpret the results after training and testing)

5. Continuous data scaling.

Next all the continuous data were scaled using a MinMaxScaler. This was done to make the machine learning training more efficient and as it is standard practice to scale the data.

6. High correlated columns 

Finally, a method was created to print high correlated columns to see if we are able to reduce some features. This is just a method that prints out the correlation coefficients so that I can manually inspect and decide what features to exclude. 

After consideration following categorical and continous features were used to create an X_train, y_train, X_test, y_test dataset for machine learning training. 

features = ['day_of_trans', 'hour_of_trans', 'month_of_trans', 'age', 'state', 'merchant', 'category', 'sex', 'city', 'state', 'zip', 'job', 'amt', 'lat', 'long', 'city_pop', 'merch_lat', 'merch_long']

```
#initialize class
fe = Feature_Extractor()

#extract data
train_df, test_df = fe.extract(training_pq_dir, testing_pq_dir)

#transform data
data, column_mappings = fe.transform(train_df, test_df)

#show results
results = fe.describe(column_mapper = column_mappings)
print(results)

-- output -- 

{'version': 'v1.0', 'Column Mapper path': '../data_sources/column_mapper_v1.0.txt', 'description': {'X_train shape': (1186297, 14), 'y_train shape': (1186297,), 'X_test shape': (296575, 14), 'y_test shape': (296575,), 'Training Features': ['state', 'merchant', 'category', 'sex', 'city', 'state', 'zip', 'job', 'amt', 'lat', 'long', 'city_pop', 'merch_lat', 'merch_long']}}

```