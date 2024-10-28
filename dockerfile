FROM python:3.10.15

ENV PYTHONPATH=/app

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .
