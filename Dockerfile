FROM python:3.7
ENV PYTHONUNBUFFERED 1

RUN mkdir /src
WORKDIR /src

RUN pip install pipenv

COPY ["Pipfile", "Pipfile.lock", "/src/"]
RUN pipenv install --system --dev
