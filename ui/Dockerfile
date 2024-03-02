FROM node:18-bookworm as ui
RUN mkdir -p /code
COPY ./*.json ./*.cjs ./*.ts /code/
WORKDIR /code
RUN npm ci --legacy-peer-deps
COPY ./ /code/
RUN mkdir -p /code/node_modules 
LABEL org.opencontainers.image.source https://github.com/noah-witt/trivia
ENTRYPOINT [ "npx", "vue-cli-service", "serve", "--port", "80", "--host", "0.0.0.0"]

FROM ui as ui-build
RUN npm run build

FROM nginx:1 as prod
COPY --from=ui-build /code/dist/ /www/site/
COPY ../nginx.prod.conf /etc/nginx/nginx.conf
LABEL org.opencontainers.image.source https://github.com/noah-witt/trivia
