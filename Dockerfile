# Base Image
FROM python:3.12-slim

# Prevent .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Show logs instantly
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Expose port
EXPOSE 8000

# Start server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]