# Use the latest Ubuntu image
FROM ubuntu:latest

# Set the working directory
WORKDIR /python-docker

# Update the package list and install Python and pip
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Create and activate the virtual environment, and install Python dependencies
RUN python3 -m venv flaskenv && \
    . flaskenv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the application port
EXPOSE 5000

# Command to run the application
CMD ["/python-docker/flaskenv/bin/flask", "run", "--host=0.0.0.0"]
