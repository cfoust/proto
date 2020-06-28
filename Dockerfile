FROM python:3.9.0b3

RUN apt-get update && \
  apt-get install build-essential && \
  rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt
