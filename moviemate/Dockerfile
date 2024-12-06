# Use a lightweight Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /moviemate

# Copy the requirements file first to leverage Docker's caching mechanism
COPY requirements.txt .

# Install system dependencies required for building wheels
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libpython3-dev \
    cython3 \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the application port
EXPOSE 3001

# Set the command to run your application
CMD ["python", "app.py"]

