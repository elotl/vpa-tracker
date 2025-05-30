FROM python:3.11-slim

# Install dependencies
RUN pip install --no-cache-dir kubernetes prometheus_client

# Set working directory
WORKDIR /app

# Copy the exporter script
COPY vpa_exporter.py .

# Set entrypoint
ENTRYPOINT ["python", "vpa_exporter.py"]

