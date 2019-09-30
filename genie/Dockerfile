# Build stage
FROM node:8.16.1-alpine as build

RUN apk update && \
    apk add --no-cache make gcc g++ python
RUN mkdir /app
COPY package*.json /app/

WORKDIR /app
RUN npm install --production --silent && \
    apk del make gcc g++ python
COPY . /app/

EXPOSE 4000
EXPOSE 4440
