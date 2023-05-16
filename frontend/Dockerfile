FROM node:20

WORKDIR /frontend

COPY ./package.json /frontend/package.json

COPY ./package-lock.json /frontend/package-lock.json

RUN npm install

COPY . /frontend
