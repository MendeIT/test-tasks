FROM python:3.12-slim-bookworm

WORKDIR /app

RUN apt-get update && \
    apt-get install -y \
    libpq-dev \
    python3-dev gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install -r requirements.txt --no-cache-dir

COPY . .

CMD bash -c "uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"