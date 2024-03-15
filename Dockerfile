FROM python:3.9

WORKDIR /app

# Copy the entire application directory into the container
COPY . .

# Set up any environment variables if needed
ENV GUNICORN_CMD_ARGS=""

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run your application using Gunicorn
CMD ["gunicorn", "-c", "gunicorn_config.py", "main:app"]
