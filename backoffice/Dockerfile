# Build stage
FROM node:8.16.1-alpine as build

RUN apk update && \
    apk add --no-cache make gcc g++ python && \
    npm install -g http-server
RUN mkdir /app
COPY . /app/

WORKDIR /app
RUN npm install --silent && \ 
    npm run build && \
    apk del make gcc g++ python

EXPOSE 8080
