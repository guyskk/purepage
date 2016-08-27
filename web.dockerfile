FROM daocloud.io/node:latest
RUN npm install -g cnpm --registry=https://registry.npm.taobao.org
WORKDIR /web
CMD cnpm install && npm run build
