FROM python:3.10

WORKDIR /backend

COPY ./requirements.txt /backend/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /backend/app