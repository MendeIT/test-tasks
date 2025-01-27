FROM python:3.12-alpine

WORKDIR /app

RUN apk update && apk add --no-cache \
    postgresql-dev gcc musl-dev \
    && pip install --upgrade pip

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["fastapi", "dev", "main.py"]