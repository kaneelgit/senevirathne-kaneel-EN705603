# SecureBank - Fraud Detection System

## Description
SecureBank is a machine learning-based software system designed to detect fraudulent transactions in banking operations.

## Table of Contents
- Prerequisites.
- Installation.
- Example usage.

## Prerequisites
This system uses Docker to containerize and run the application. Ensure Docker is installed on your machine before proceeding.

## Installation
Follow the steps below to set up and run the application:

1. **Clone the repository:**
```bash
git clone https://github.com/creating-ai-enabled-systems-fall-2024/senevirathne-kaneel.git
```
2. **Navigate to the ```securebank``` directory:**
```bash
cd securebank
```
3. **Build the Docker image. Replace ```<appname>``` with the desired name for your application (e.g., ```flask-app```):**
```bash
docker build -t <appname>:latest .
```
## Example Usage 

1. **Running the Application:** Go to the securebank folder and run the application using Docker. Make sure to replace ```<appname>``` with the name of the Docker image you built in the previous step.
```bash
docker run -p 5000:5000 <appname>
```
2. **Running Inference:** You can perform a prediction on a sample data file (e.g., test.json) using curl. Replace the path to test.json if necessary.
```bash
curl -X POST http://127.0.0.1:5000/predict -H "Content-Type: application/json" -d @test.json
```
This will return the output in the terminal. For example:
```makefile
Transaction Approved.
Model: random forest_v1
```
3. **Reading model details:** You can read all available models and their performance details using curl. Type the following in the terminal to get model details.
```bash
curl -X POST http://127.0.0.1:5000/get_history
```
This will return the output in the terminal. For example: 
```makefile
              Model Version  Precision   Recall  Accuracy
logistic_regression      v1   0.059038 0.730645  0.946855
      random forest      v1   0.121898 0.625806  0.978223
                lda      v1   0.104839 0.650000  0.973683
     sgd_classifier      v1   0.064606 0.745161  0.950740
```

4. **Selecting a model:** After reading model details, you can select a model using the model and the version of the model. For example to select the sgd_classifier model version 1, replace "logistic_regression_v1" in the curl command below with "sgd_classifier_v1". 

```bash
curl -X POST http://127.0.0.1:5000/select_model -H "Content-Type: application/json" -d '{"model_name": "logistic_regression_v1"}'
```
This will return the output in the terminal. For example:
```makefile
Selected model: logistic_regression_v1
```
5. **Generating a new dataset:** This function generates a new dataset. Dataset split, random state and the version of the dataset should be given. (e.g. 70, 50, "v2"). This will create a new training and testing dataset with the respective version.

```bash
curl -X POST http://127.0.0.1:5000/generate_new_dataset -H "Content-Type: application/json" -d '{"split": 70, "random_state": 50, "version": "v2"}'
```
This will return a description of the dataset in the terminal. For example: 
```makefile
{"Test default storage":"data_sources/test_data_v2.parquet","Train default storage":"data_sources/train_data_v2.parquet","description":{"No. Test Samples":127286,"No. Train Samples":1355586,"Train set fraud/no fraud split":"5926 / 1349660","fraud/no fraud split":"570 / 126716"},"version":"v2"}
```

6. **Requesting a dataset description:** This function will get the dataset description given the dataset version. The following curl function gives the description of the dataset "v2". Replace "v2" with the dataset version to see details of other datasets. 
```bash
curl -X GET http://127.0.0.1:5000/get_dataset_description?version=v2
```
This will return the requested dataset description. For example: 
```makefile
Train default storage: data_sources/train_data_v2.parquet
Test default storage: data_sources/test_data_v2.parquet
description: {'No. Train Samples': 1355586, 'Train set fraud/no fraud split': '5926 / 1349660', 'No. Test Samples': 127286, 'fraud/no fraud split': '570 / 126716'}
```
