import pandas as pd


class Pipeline:

    def __init__(self):
        pass
    
    def load_dataset(self, file_path, column_names = None):
        """
        Loads dataset given file_path
        """
        if column_names:
            df = pd.read_csv(file_path, header = None)
            df.columns = column_names
        else:
            df = pd.read_csv(file_path, header = None)

        return df

    def partition_data(self, ratings_df, partition_type = None):
        """
        Partitions dataset given partition type
        """
        pass

if __name__ == "__main__":
    pline = Pipeline()
    df = pline.load_dataset('storage/u.data')