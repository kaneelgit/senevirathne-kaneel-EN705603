from sklearn.model_selection import train_test_split
import pandas 

class Dataset_designer:

    def extract(self, raw_dataset_filename: str):
        """
        This method inputs a raw dataset filename and opens a parquet format file. If another file format is given it raises an error.

        """
        if raw_dataset_filename.endswith('.parquet'):
            return pandas.read_parquet(raw_dataset_filename)
        else:
            raise ValueError("Only parquet files are allowed.")
            
    
    def sample(self, raw_dataset: pandas.DataFrame, test_split: float = 0.1, random_state: int = 42):
        """
        This method inputs a pandas dataframe and the test split ratio and split it into training and testing sets. 
        It outputs the test and training sets. 
        """
        # # Ensure test_split is between 0 and 1
        # if not (0 < test_split < 1):
        #     raise ValueError("test_split must be a float between 0 and 1")

        # # Perform train-test split
        # self.raw_train, self.raw_test = train_test_split(raw_dataset, test_size=test_split, random_state=random_state)

        # Extract unique cc_num values
        unique_cc_nums = raw_dataset['cc_num'].unique()

        # import pdb; pdb.set_trace()
        # Perform train-test split on unique cc_num values
        train_cc_nums, test_cc_nums = train_test_split(unique_cc_nums, test_size=test_split, random_state=random_state)

        # Create train and test sets based on the split cc_num values
        self.raw_train = raw_dataset[raw_dataset['cc_num'].isin(train_cc_nums)]
        self.raw_test = raw_dataset[raw_dataset['cc_num'].isin(test_cc_nums)]

        return [self.raw_train, self.raw_test]
    
    def describe(self, *args, **kwargs):

        version = kwargs.get('version', 'v1.0')
        train_storage_path = kwargs.get('Train Storage', f'../data_sources/train_data_{version}.parquet')
        test_storage_path = kwargs.get('Test Storage', f'../data_sources/test_data_{version}.parquet')

        #important columns 
        data_description = {}
        data_description['No. Train Samples'] = len(self.raw_train)
        data_description['Train set fraud/no fraud split'] = f"{self.raw_train['is_fraud'].value_counts()[1]} / {self.raw_train['is_fraud'].value_counts()[0]}"
        data_description['No. Test Samples'] = len(self.raw_test)
        data_description['fraud/no fraud split'] = f"{self.raw_test['is_fraud'].value_counts()[1]} / {self.raw_test['is_fraud'].value_counts()[0]}"

        result = {
            'version': version,
            'Train default storage': train_storage_path,
            'Test default storage': test_storage_path,
            'description': data_description
        }
        
        return result
    
    def load(self, data_list: list, train_output_filename: str, test_output_filename:str):
        """
        Saves the transformed data to a parquet file.
        """
        data_list[0].to_parquet(train_output_filename, index=False)
        print(f"Train data saved to {train_output_filename}")
        data_list[1].to_parquet(test_output_filename, index=False)
        print(f"Test data saved to {test_output_filename}")

# dd = Dataset_designer()
# raw_data = dd.extract('../data_sources/raw_data_v1.0.parquet')
# data = dd.sample(raw_data, random_state = 50)


# import pdb; pdb.set_trace()