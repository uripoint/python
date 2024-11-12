FROM python:3.9-slim

WORKDIR /app

# Install required system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application code
COPY task_producer.py .
COPY task_worker.py .
COPY result_collector.py .

# Environment variable to determine which component to run
ENV COMPONENT=producer

# Run the appropriate component based on COMPONENT env var
CMD if [ "$COMPONENT" = "producer" ]; then \
        python task_producer.py; \
    elif [ "$COMPONENT" = "worker" ]; then \
        python task_worker.py; \
    elif [ "$COMPONENT" = "collector" ]; then \
        python result_collector.py; \
    else \
        echo "Invalid component specified"; \
        exit 1; \
    fi
