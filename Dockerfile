# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the Pipfile and Pipfile.lock to the container
COPY app/requirements.txt ./

# Install pipenv and compile dependencies
RUN pip install -r requirements.txt
# Copy the rest of the backend code into the container
COPY app /app

# Expose the port that the app runs on
EXPOSE $PORT

# Command to run the app with uvicorn
CMD ["sh", "-c", "cd /app && uvicorn main:app --host 0.0.0.0 --port $PORT --reload"]
