import pandas as pd
from sklearn.model_selection import train_test_split

class Pipeline:

    def __init__(self):
        pass
    
    def load_dataset(self, file_path, column_names = None):
        """
        Loads dataset given file_path
        """
        if column_names:
            df = pd.read_csv(file_path, sep = '\t', engine = 'python', header = None)
            df.columns = column_names
        else:
            df = pd.read_csv(file_path, sep = '\t', engine = 'python', header = None)

        return df

    def partition_data(self, data, partition_type = None, test_size = 0.2):
        """
        Partitions dataset given partition type
        """

        if partition_type == "stratified":
             
            # Split data based on unique user IDs
            unique_users = data['user'].unique()
            train_users, test_users = train_test_split(unique_users, test_size=test_size, random_state=42)

            # Create train and test sets based on user_id
            train_data = data[data['user'].isin(train_users)]
            test_data = data[data['user'].isin(test_users)]

            return train_data, test_data
        
        elif partition_type == "temporal":
            data = data.sort_values(by = 'timestamp').reset_index(drop = True)
            train_data, test_data = train_test_split(data, test_size = 0.2, shuffle = False)

            return train_data, test_data

        else:
            train_data, test_data = train_test_split(data, test_size=test_size, random_state=42)

            return train_data, test_data

# if __name__ == "__main__":
#     pline = Pipeline()
#     cols = ['user_id', 'item_id', 'rating', 'timestamp']
#     df = pline.load_dataset('storage/u.data', column_names = cols)
#     import pdb; pdb.set_trace()