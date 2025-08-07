# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the working directory
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application's source code to the container
COPY . .

# Define the command to run your app
CMD ["gunicorn", "-b", "0.0.0.0:8080", "main:handle_request"]