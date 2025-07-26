# Use a specific, lightweight Python image compatible with linux/amd64 [cite: 56, 57]
FROM --platform=linux/amd64 python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all the source code into the container
COPY src/ .

# This command will run when the container starts
CMD ["python", "main.py"]