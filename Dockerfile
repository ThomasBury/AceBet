# Use the official Python base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the application code into the container
COPY . acebet

# Install the application package
RUN pip install --upgrade pip
RUN pip install -U ./acebet

# Expose the port that the FastAPI app will run on
EXPOSE 80

# Run the FastAPI app using the full path to the module
CMD ["uvicorn", "acebet.app.main:app", "--host", "0.0.0.0", "--port", "80"]
