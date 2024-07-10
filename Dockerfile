# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y build-essential libpq-dev \
    && apt-get clean

# Install pip
RUN pip install --upgrade pip

# Copy the requirements file into the image
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the application code into the image
COPY ./expense_tracker /app/

# Expose the port the app runs on
EXPOSE 8000

# Command to run the migrations and then the app
CMD ["sh", "-c", "python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:8000"]
