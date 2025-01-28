FROM python:3.11.11-alpine3.21

WORKDIR /usr

# copy project
COPY . .

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./src/requirements.txt .
RUN pip install -r src/requirements.txt

WORKDIR /usr/src
