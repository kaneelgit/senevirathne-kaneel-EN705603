# Securebank - Fraud Detection System

## Description
This is a software system used to detect fraud in a bank transactions using machine learning. 

## Table of Contents
- Prerequisites.
- Installing.
- Running the app.
- Usage with examples.

## Prerequisite 
The software is using docker to run the system. Docker must be installed in your machine in order to run the system. 

## Installation
Here are step-by-step instructions on how to get the app running.

Clone repository
```bash
git clone https://github.com/creating-ai-enabled-systems-fall-2024/senevirathne-kaneel.git
```
Change directory to application folder
```bash
cd securebank
```
Build docker image
```bash
docker build -t <appname>:latest .
```
## Example Usage 

Go to the securebank folder and run the application using docker.
```bash
cd securebank

docker run -p 5000:5000 <appname>
```

Run inference on a testig data sample. (test.json)
```bash
curl -X POST http://127.0.0.1:5000/predict -H "Content-Type: application/json" -d @test.json
```
This will return the output in the terminal in the following format. 
```
{
Transaction Approved.
Model: random forest_v1
}
```