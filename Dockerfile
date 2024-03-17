# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy only the requirements.txt file to the container
COPY requirements.txt /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files into the container
COPY . /app

# Expose port 5500 to the outside world
EXPOSE 5500

# Define environment variable
ENV FLASK_APP=main.py

# Run gunicorn with the configured settings
CMD ["gunicorn", "-c", "gunicorn_config.py", "main:app"]
