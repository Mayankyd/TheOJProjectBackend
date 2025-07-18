# Use official Python base image
FROM python:3.11-slim

# Install system packages: gcc (for Python), C++ and Java compilers
RUN apt-get update && apt-get install -y \
    gcc g++ openjdk-17-jdk \
    && rm -rf /var/lib/apt/lists/*

# Set working directory inside container
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose port
EXPOSE 8000

# Run Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
