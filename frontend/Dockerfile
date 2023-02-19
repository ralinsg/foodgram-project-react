# build env
FROM node:13.12.0-alpine as build
LABEL author="ralinsg" version='0.1.f.' release_date='18.02.2023'
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . ./
RUN npm run build
CMD cp -r build result_build
