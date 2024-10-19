# Use the official Python base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . .

# Install the application package
RUN pip install --upgrade pip \
    && pip install .\
    && pip install fastapi uvicorn -U

# Set PYTHONPATH so Python can find the module
ENV PYTHONPATH=/app/src

# Run the FastAPI app using the full path to the module
CMD ["uvicorn", "src.acebet.app.main:app", "--host", "0.0.0.0", "--port", "80"]
