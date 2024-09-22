# Project Name
Securebank - Fraud Detection System

## Description
This is a software system used to detect fraud in a bank transactions using machine learning. 

## Table of Contents
- Prerequisite
- Installation
- Usage

## Prerequisite 
The software is using docker to run the system. Docker must be installed in your machine in order to run the system. 

## Installation
Step-by-step instructions on how to get the development environment running.

```bash
#clone repository
git clone https://github.com/creating-ai-enabled-systems-fall-2024/senevirathne-kaneel.git
#change directory to application folder
cd securebank
#build docker image
docker build -t <appname>:latest .
```

## Usage 

```bash
#run docker app
docker run -p 5000:5000 <appname>

#test the sample file
