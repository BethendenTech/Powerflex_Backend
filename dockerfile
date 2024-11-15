# Start with a base image (such as Python with Debian for compatibility with PostgreSQL)
FROM python:3.10-slim

# Install required system dependencies for PostgreSQL
RUN apt-get update && apt-get install -y \
    postgresql postgresql-contrib libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables for PostgreSQL (optional)
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_DB=powerflex

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Set up PostgreSQL
RUN service postgresql start && \
    su postgres -c "psql -c \"CREATE USER $POSTGRES_USER WITH PASSWORD '$POSTGRES_PASSWORD';\"" && \
    su postgres -c "psql -c \"CREATE DATABASE $POSTGRES_DB OWNER $POSTGRES_USER;\"" && \
    su postgres -c "psql -c \"GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DB TO $POSTGRES_USER;\""

# Copy your application code
COPY . /app
WORKDIR /app

# Run a script to start both PostgreSQL and your app
CMD service postgresql start && python manage.py
