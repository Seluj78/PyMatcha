FROM node:12.2.0-alpine

WORKDIR /frontend

ENV PATH /frontend/node_modules/.bin:$PATH

COPY frontend/package.json /frontend/package.json
COPY frontend/yarn.lock /frontend/yarn.lock
COPY ./frontend .

RUN yarn install

RUN yarn build

CMD ["serve", "-s", "dist"]
