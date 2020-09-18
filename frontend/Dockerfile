FROM node:12.2.0-alpine

WORKDIR /frontend

ENV PATH /frontend/node_modules/.bin:$PATH

COPY package.json /frontend/package.json
RUN yarn install
RUN yarn global add @vue/cli

CMD ["yarn", "serve"]
