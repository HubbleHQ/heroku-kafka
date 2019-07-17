FROM python:3.7
ENV PYTHONUNBUFFERED 1

RUN mkdir /src
WORKDIR /src

COPY . .
RUN pip install -r requirements.txt
