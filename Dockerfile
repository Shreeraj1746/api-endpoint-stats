FROM python:3.11-slim

WORKDIR /app

# Install PostgreSQL client and build dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies using bind mount
RUN --mount=type=bind,source=requirements.txt,target=/tmp/requirements.txt \
    --mount=type=bind,source=requirements-test.txt,target=/tmp/requirements-test.txt \
    pip install --no-cache-dir -r /tmp/requirements.txt -r /tmp/requirements-test.txt

# Copy application file
COPY app.py .

# Copy test files - needed for running tests
COPY tests/ ./tests/
COPY pytest.ini .

ENV FLASK_APP=app.py
ENV FLASK_ENV=development
ENV PYTHONUNBUFFERED=1

EXPOSE 9999

CMD ["python", "app.py"]
