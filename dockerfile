FROM python:3.10.15

ENV PYTHONPATH=/app/fed-multimodal-restcol

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt
