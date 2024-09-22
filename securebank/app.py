from flask import Flask, request, jsonify, Response
import pipeline
from modules import dataset_design, feature_extractor
import json
import pandas as pd
import joblib
import warnings
warnings.filterwarnings("ignore")
import datetime
import plotille

from sklearn.metrics import precision_score, recall_score

app = Flask(__name__)

model_pipeline = pipeline.Pipeline()


@app.route('/')
def home():
    return "hello world"

@app.route('/predict', methods = ["POST"])
def predict():
    global model_pipeline
    data = request.get_json()
    data = model_pipeline.predict(data)
    return data

@app.route('/select_model', methods = ["POST"])
def select_model():
    global model_pipeline
    model_name = request.json.get('model_name')
    model_pipeline = pipeline.Pipeline(model_name)
    return f"Selected model: {model_name}\n"

@app.route('/get_history', methods = ["POST"])
def get_history():
    global model_pipeline    
    history_df = model_pipeline.get_history()
     # Print the DataFrame in a more readable format
    print("Model History DataFrame:")
    print(history_df.to_string(index=False))  # Prints DataFrame without the index
    
    # Return the HTML for the client
    return history_df.to_string(index=False) + '\n'

@app.route('/generate_new_dataset', methods=["POST"])
def generate_new_dataset():
    """
    Create a new dataset and save dataset description.
    """
    data_dict = request.get_json()

    dd = dataset_design.Dataset_designer()
    raw_df = dd.extract("data_sources/raw_data_v1.0.parquet")

    #get dataset split and random state
    split = data_dict['split']
    random_state = data_dict['random_state']
    version = data_dict['version']

    #extract data
    data_list = dd.sample(raw_df, test_split = split, random_state = random_state)
    desc = dd.describe(version = version, Train_Storage = f'data_sources/train_data_{version}.parquet', Test_Storage = f'data_sources/test_data_{version}.parquet')
    dd.load(data_list, desc['Train default storage'], desc['Test default storage'])

    #save data dictionary
    with open(f"data_sources/data_description_{version}.txt", "w") as file:
        for key, value in desc.items():
            file.write(f"{key}: {value}\n")

    return desc

@app.route('/get_dataset_description', methods=["GET"])
def get_dataset_description():
    
    #get version from reqeust
    version = request.args.get('version')

    #get version dictionary.
    with open(f"data_sources/data_description_{version}.txt", "r") as file:
        data = file.read()

    return data

@app.route('/audit_performance', methods = ["GET"])
def audit_performance():

    # dataset version
    model_name = request.args.get('model_name')
    dataset_version = request.args.get('dataset_version')

    #get the specific model name and version
    model = model_name.split('_')[0]
    model_version = model_name.split('_')[1]
    
    #get the dataset to test the model
    train_data_dir = f"data_sources/train_data_{dataset_version}.parquet"
    train_df = pd.read_parquet(train_data_dir)
    test_data_dir = f"data_sources/test_data_{dataset_version}.parquet" 
    test_df = pd.read_parquet(test_data_dir)

    #extract feautures to audit the model
    fe = feature_extractor.Feature_Extractor()
    data_train_test, _ = fe.transform(train_df, test_df)

    #get the test dataset
    _, _, X_test, y_test = data_train_test

    #load the model
    model_dir = f"storage/models/artifacts/{model_name}.pkl"
    model_ = joblib.load(model_dir)

    #y predict
    y_pred = model_.predict(X_test)

    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    # prec = 0.1
    # rec = 0.7

    #print results
    print(f"precision score: {prec}")
    print(f"Recall score: {rec}")

    #get past data
    #get model performance history dataframe
    df = pd.read_csv('storage/performance_history.csv')
    df_data = df[(df['model_name'] == model) & (df['model_version'] == model_version)]

    # Initialize lists to store precision and recall values and dates
    precision_values = []
    precision_dates = []
    recall_values = []
    recall_dates = []

    # Iterate over the columns of the DataFrame
    for column in df_data.columns:
        if column.startswith('precision_'):
            # Extract date from column name and append to precision_dates
            date = column.split('_')[1]
            precision_dates.append(date)
            # Append precision value to precision_values
            precision_values.append(df[column][0])
        elif column.startswith('recall_'):
            # Extract date from column name and append to recall_dates
            date = column.split('_')[1]
            recall_dates.append(date)
            # Append recall value to recall_values
            recall_values.append(df[column][0])

    #add newest data
    todays_date = str(datetime.datetime.now().date()).replace('-', '')

    #add to precision values
    precision_values.append(prec)
    precision_dates.append(todays_date)

    #add to recall values
    recall_values.append(rec)
    recall_dates.append(todays_date)

    # Mapping dates to x-axis indices (we can't directly use strings on x-axis in plotille)
    x_indices = list(range(len(precision_dates)))

    # Create an ASCII plot using plotille
    fig = plotille.Figure()
    fig.width = 60
    fig.height = 20
    fig.set_x_limits(min_=0, max_=len(x_indices))  # Using indices for x-axis
    fig.set_y_limits(min_=0, max_=1)  # Adjust based on your metrics scale

    # Add precision and recall data to the plot
    fig.plot(x_indices, precision_values, label="Precision")
    fig.plot(x_indices, recall_values, label="Recall")

    fig.title = "Model Precision and Recall"
    fig.xlabel = "Dates"
    fig.ylabel = "Metrics"

    # Format the x-ticks with date strings
    fig.x_ticks = [(i, int(date)) for i, date in enumerate(precision_dates)]

    # Generate the ASCII plot
    ascii_plot = fig.show(legend=True)

    # Add a newline after the plot
    ascii_plot_with_newline = '\n' + f"Model precision: {prec}" + "\n" + f"Model Recall: {rec}" + '\n' + "\n" + "Model Performance Over Time" + '\n' + ascii_plot + "\n"

    # Return the ASCII plot as plain text
    return Response(ascii_plot_with_newline, mimetype='text/plain') 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
