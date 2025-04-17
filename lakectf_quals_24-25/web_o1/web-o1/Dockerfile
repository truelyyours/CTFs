# Use the official Python slim image as the base
FROM python:3.9-slim

# Install Node.js (version 18.x) and other dependencies
RUN apt-get update && \
    apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Python application files
COPY app1.py app2.py ./

# Copy Node.js application file
COPY app3.js ./

# Initialize Node.js project and install Express
RUN npm init -y && \
    npm install express

# Copy the startup script and make it executable
COPY start.sh .
RUN chmod +x start.sh

# Expose port 9222 (only the first proxy is exposed)
EXPOSE 9222

# Define the default command to run the startup script
CMD ["./start.sh"]
