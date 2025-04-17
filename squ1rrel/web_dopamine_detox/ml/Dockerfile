# Use an official Python base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg gcc libsndfile1 && \
    rm -rf /var/lib/apt/lists/*

# Copy the application files
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install flask gunicorn torch torchaudio pydub numpy

# Create upload folder
RUN mkdir -p uploads

# Expose port 8050
EXPOSE 8050

# Command to run the app using gunicorn on port 8050
CMD ["python3", "-m", "gunicorn", "--workers", "4", "-b", "0.0.0.0:8050", "app:app"]
