FROM python:3.9.0b3-alpine3.12

ENV PYTHONPATH "/usr/local/lib/python3.9/dist-packages:/app/proto:/app/proto/vendor/anki"

COPY requirements.txt .
RUN pip install -r requirements.txt
