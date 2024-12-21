FROM python:3.11-slim

WORKDIR /app
EXPOSE 8000

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    python3-pip \
    libpq-dev \
    sqlite3 \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*


# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Run migrations and start server
CMD python manage.py migrate && \
    python manage.py collectstatic --no-input
    # gunicorn vault.wsgi:application \
    # --bind 0.0.0.0:8000 \
    # --certfile=cert/cert.pem \
    # --keyfile=cert/key.pem \
    # --ssl-version=TLSv1_2 