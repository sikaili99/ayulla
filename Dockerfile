FROM python:3.9-slim-buster

# Install OS dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
        && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Install SQLite and its dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        sqlite3 \
        && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the Django app code into the container
COPY . .

# Create an empty SQLite database file
RUN touch db.sqlite3
RUN chmod 777 db.sqlite3

# Run migrations and migrate
RUN python manage.py makemigrations
RUN python manage.py migrate

# Expose the port on which the app will run
EXPOSE 8080

# Run the Django app with Gunicorn
CMD ["gunicorn", "ayulla.wsgi:application", "--bind", "0.0.0.0:8080"]
