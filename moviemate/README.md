# Moviemate - Recommendation System

## Description

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
cd moviemate
```
3. **Build the Docker image. Replace ```<appname>``` with the desired name for your application (e.g., ```flask-app```):**
```bash
docker build -t <appname>:latest .
```
## Example Usage 
