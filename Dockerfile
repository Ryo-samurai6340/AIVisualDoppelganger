# Use the official Python image as a base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port that your app runs on
EXPOSE 5500

# Command to run your application using Gunicorn
CMD ["gunicorn", "-c", "gunicorn_config.py", "main:app"]
