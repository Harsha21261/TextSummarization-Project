FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update -y && apt-get install -y build-essential libpq-dev

COPY . /app

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --upgrade accelerate

# Expose port
EXPOSE 8000

# Start the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
