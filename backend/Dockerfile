FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /backend

COPY ./requirements.txt /backend/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /backend/app