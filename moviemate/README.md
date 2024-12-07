# Moviemate - Recommendation System

## Description

Moviemate is a movie recommendation system designed to provide personalized movie suggestions to users. Packaged with Docker for easy deployment and scalability, it offers a range of features, including the ability to add new users, update the underlying recommendation model, and generate tailored movie recommendations. 

## Table of Contents
- Prerequisites.
- Installation.
- Example usage.

## Prerequisites
This interface system uses Docker to containerize and run the application. Ensure Docker is installed on your machine before proceeding. 

## Installation
Follow the steps below to set up and run the application:

1. **Clone the repository:**
```bash
git clone https://github.com/creating-ai-enabled-systems-fall-2024/senevirathne-kaneel.git 
```
2. **Navigate to the ```moviemate``` directory:**
```bash
cd moviemate
```
3. **Build the Docker image. Replace ```<appname>``` with the desired name for your application (e.g., ```flask-app```):**
```bash
docker build -t <appname>:latest .
```
## Example Usage 

To test the recommendation system, follow these steps:

1. Start the application.
Run the following command in your terminal to start the application:
```bash
docker run -p 5000:5000 -it <appname>
```
2. Interact with the system.
Once the application is running, open a new terminal window and use the curl command to interact with the system's endpoints. The system allows you to:
- Get recommendations.
- Add new users.
- Retrain the recommendation model.

3. Get Recommendations.
To get a recommendation you can use the following command.
```bash
curl -X GET "http://localhost:5000/recommend?user_id=<user_id>"
```
Replace ``<user_id>`` with the desired user.

This return the top 10 recommendations for specific user.
```
{"recommendations":["Raiders of the Lost Ark (1981)","Return of the Jedi (1983)","Star Wars (1977)","Titanic (1997)","Empire Strikes Back, The (1980)","Gone with the Wind (1939)","Schindler's List (1993)","Back to the Future (1985)","Lawrence of Arabia (1962)","Indiana Jones and the Last Crusade (1989)"]}
```

4. Add a New User
To add a new user, prepare a JSON file with the following format:
```
{
"age": 25,
"gender": "F",
"occupation": "other",
"ratings": {},
"zip code": 21201
}
```
- The JSON should include the user's age, gender, occupation, zip code, and ratings (if available).
- If no ratings are available, use an empty dictionary for "ratings".

Then use the add_user endpoint to add this new user to the database.
```
curl -X POST http://127.0.0.1:5000/add_user -H "Content-Type: application/json" -d @new_user.json
```

Once a user is added, they are assigned a unique user_id. An example of the updated database after adding a new user might look like this:
```
941|20|M|student|97229
942|48|F|librarian|78209
943|22|M|student|77841
944|25|F|other|21201 --> NEW ENTRY
```