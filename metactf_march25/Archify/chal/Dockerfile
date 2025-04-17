FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy application files
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Install zip
RUN apt-get update && apt-get install -y zip

# Seed the database during runtime
CMD ["sh", "-c", "python app.py"]
