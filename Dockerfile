FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

COPY . /app

# Install system libraries required for WeasyPrint
RUN apt-get update && apt-get install -y \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    libgirepository1.0-dev

# Install any needed packages specified in requirements.txt
# Note: The requirements.txt file must be present in the directory where you build the Docker image
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_ENV=development
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0

# Command to run the Flask application
CMD ["flask", "run"]
