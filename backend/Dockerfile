FROM python:3.13-slim
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .
COPY .env .env

# Create directory for Google credentials
RUN mkdir -p /app/credentials

# Expose the port the app runs on
EXPOSE 8001

# Command to run the application
CMD ["python", "main.py"]