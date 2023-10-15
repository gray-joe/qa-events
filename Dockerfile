# Use the official Python image as the base image
FROM python:3.11-slim

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Install system dependencies, including PostgreSQL development packages
RUN apt-get update && \
    apt-get install -y \
        build-essential \
        libpq-dev && \
    apt-get clean

# Install Python dependencies
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the application code into the container
COPY . .

# Add execute permission to the wait-for-it.sh script
RUN chmod +x wait-for-it.sh

# Expose the port your Flask app runs on (e.g., 5000)
EXPOSE 5000

# Run the Flask application
CMD ["./wait-for-it.sh", "db:5432", "--", "flask", "run", "--host=0.0.0.0"]
