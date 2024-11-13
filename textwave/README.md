# TextWave - Question Answer System

## Description
Textwave is a text-based question-answering system designed for querying institutional data. It utilizes a FAISS index to embed this data, enabling efficient k-nearest neighbor searches. Once the relevant data is retrieved, Textwave employs the MISTRAL AI API to generate a detailed and accurate response using generative AI.

## Table of Contents
- Prerequisites.
- Installation.
- Example usage.

## Prerequisites
This interface system uses Docker to containerize and run the application. Ensure Docker is installed on your machine before proceeding. The embedding system uses python3, transformers and mistralai. Ensure these libraries and services are installed on your machine before proceeding. The requirements.txt file is available to see what modules are needed.

## Installation
Follow the steps below to set up and run the application:

1. **Clone the repository:**
```bash
git clone https://github.com/creating-ai-enabled-systems-fall-2024/senevirathne-kaneel.git 
```
2. **Navigate to the ```textwave``` directory:**
```bash
cd textwave
```
3. **Build the Docker image. Replace ```<appname>``` with the desired name for your application (e.g., ```flask-app```):**
```bash
docker build -t <appname>:latest .
```
## Example Usage 

### Question Answer Service ###

To test the question-answering system, first start it by running the following command in your terminal: 
```bash
docker run -p 3001:3001 -it <appname>
```
Once the app is running, open a new terminal window and use the curl command to query the system. The request requires a JSON file containing the query, the number of nearest neighbors (k), and the MISTRAL API key.

Here’s the curl command to send the request:
```bash
curl -X POST http://127.0.0.1:3001/query -H "Content-Type: application/json" -d @<sample_query_file.json>
```
A sample JSON file, such as sample_query_file.json, should look like this:
```json
{
    "query": "Who is Abraham Lincoln?",
    "api_key": "xxxxxxxxxxxxxxxxxxxxxx",
    "k": 5
}
```
Replace "xxxxxxxxxxxxxxxxxxxxxx" with your actual API key and save this file in the same directory as your terminal, then execute the command to test the question-answering system.