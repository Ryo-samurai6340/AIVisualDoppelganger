# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5500 to the outside world
EXPOSE 5500

# Define environment variable
ENV FLASK_APP=main.py

# Run gunicorn with the configured settings
CMD ["gunicorn", "-c", "gunicorn_config.py", "main:app"]
