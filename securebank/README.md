# Securebank - Fraud Detection System

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

1. Clone the repository
```bash
git clone https://github.com/creating-ai-enabled-systems-fall-2024/senevirathne-kaneel.git
```
2. Navigate to the ```securebank``` directory:
```bash
cd securebank
```
3. Build the Docker image. Replace ```<appname>``` with the desired name for your application (e.g., ```flask-app```):
```bash
docker build -t <appname>:latest .
```
## Example Usage 

1. Running the Application: Go to the securebank folder and run the application using Docker. Make sure to replace ```<appname>``` with the name of the Docker image you built in the previous step.
```bash
docker run -p 5000:5000 <appname>
```
2. Running Inference: You can perform a prediction on a sample data file (e.g., test.json) using curl. Replace the path to test.json if necessary.
```bash
curl -X POST http://127.0.0.1:5000/predict -H "Content-Type: application/json" -d @test.json
```
This will return the output in the terminal. For example:
```makefile
Transaction Approved.
Model: random forest_v1
```