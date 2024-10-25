# IronClad - Visual Search System

## Description
IronClad is a visual search system that allows users to find a specific image within a database. Leveraging the 'vggface2' model for inference, it analyzes the input image to identify and return similar faces from the current gallery.

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
2. **Navigate to the ```ironclad``` directory:**
```bash
cd ironclad
```
3. **Build the Docker image. Replace ```<appname>``` with the desired name for your application (e.g., ```flask-app```):**
```bash
docker build -t <appname>:latest .
```

## Example Usage 

1. **Running the Application:** Go to the ironclad folder and run the application using Docker. Make sure to replace ```<appname>``` with the name of the Docker image you built in the previous step.
```bash
docker run -p 5000:5000 <appname>
```
2. **Identifying a Person:** Use an example image to pull matching faces from the index. An optional argument is k, the number of matching identifies you desire to pull. The default value of 5 is used if no k is provided. Example below shows how to run a file named 'Aaajohn_doe.jpg' requesting the best 6 matches (k = 6) from the system.
```bash
curl -F "file=@Aaajohn_doe.jpg" -F "k=6" http://127.0.0.1:5000/identify
```
Resuling output.
```
Matched Identities:
Aaajohn doe
Aaajohn doe
Aaajohn doe
Anna Kournikova
Adrian McPherson
Li Peng
```
3. **Adding a Person:** Add a new person to the system and the embedding to the Faiss Index. This method requires you to send an image to the system in the following format. '<First_Name>_<Last_Name>.jpg'. The system will then add the person to the index and save the image in the gallery for later use.
```bash
curl -F "file=@Aaajohn_doe.jpg"  http://127.0.0.1:5000/add
```
4. **Checking search log:** This is a method to check the request history. You can search the log by using the following command. 
```bash
curl http://127.0.0.1:5000/history
```
Sample output.
```
=== Search Logs ===

Timepoint: 2024-10-24 16:58:02
k: 10
Names: Aaron Sorkin, Anibal Ibarra, Janet Thorpe, David Heymann, William Ford Jr, David Nalbandian, Tom Cruise, Michael Douglas, Tom Cruise, Peter Bacanovic
----------------------------------------
Timepoint: 2024-10-24 16:58:17
k: 2
Names: Aaron Sorkin, Anibal Ibarra
----------------------------------------
Timepoint: 2024-10-24 16:58:24
k: 5
Names: Aaron Sorkin, Anibal Ibarra, Janet Thorpe, David Heymann, William Ford Jr
----------------------------------------
Timepoint: 2024-10-25 14:54:59
k: 5
Names: Aaajohn doe, Aaajohn doe, Anna Kournikova, Adrian McPherson, Li Peng
----------------------------------------
Timepoint: 2024-10-25 19:39:05
k: 5
Names: Aaajohn doe, Aaajohn doe, Anna Kournikova, Adrian McPherson, Li Peng
----------------------------------------
Timepoint: 2024-10-25 19:50:32
k: 3
Names: Aaajohn doe, Aaajohn doe, Aaajohn doe
----------------------------------------
Timepoint: 2024-10-25 19:50:47
k: 3
Names: Aaajohn doe, Aaajohn doe, Aaajohn doe
----------------------------------------
Timepoint: 2024-10-25 19:51:22
k: 6
Names: Aaajohn doe, Aaajohn doe, Aaajohn doe, Anna Kournikova, Adrian McPherson, Li Peng
----------------------------------------
```
