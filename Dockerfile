FROM python:3.6

ENV PYTHONPATH "/usr/local/lib/python3.6/dist-packages:/app/proto:/app/proto/vendor/anki"

COPY requirements.txt .
RUN pip install -r requirements.txt
