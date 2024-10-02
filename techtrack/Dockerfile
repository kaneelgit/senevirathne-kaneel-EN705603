# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN apt-get update && apt-get install -y ffmpeg 
    
# Install Python dependencies
RUN pip install -r requirements.txt

# Expose the UDP port
EXPOSE 23000

# Command to run the Python script
CMD ["python", "app.py"]
