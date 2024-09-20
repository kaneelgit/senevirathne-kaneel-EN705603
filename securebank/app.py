from flask import Flask, request, jsonify
import pipeline
from modules import dataset_design
import json
import pandas as pd


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
    desc = dd.describe(version = version)

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
    version = request.args.get('dataset_version')

    #get model performance history dataframe
    df = pd.read_csv('storage/performance_history.csv')

    import pdb; pdb.set_trace()

    return version


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
