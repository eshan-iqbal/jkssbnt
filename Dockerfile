FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY monitor.py .
COPY notifiers/ ./notifiers/

# Create directories for data and logs
RUN mkdir -p data logs

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the monitor
CMD ["python", "monitor.py"]
