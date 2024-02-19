FROM node:18-bookworm as ui
RUN mkdir -p /code
COPY ./ui/*.json ./ui/*.cjs ./ui/*.ts /code/
WORKDIR /code
RUN npm ci
COPY ./ui/ /code/
RUN mkdir -p /code/node_modules 
LABEL org.opencontainers.image.source https://github.com/noah-witt/sfpd-log
ENTRYPOINT [ "npx", "vite", "--port", "80", "--host", "0.0.0.0"]

FROM ui as ui-build
RUN npm run build

FROM nginx:1 as ui-prod
COPY --from=ui-build /code/dist/ /www/site/
COPY ./nginx.prod.conf /etc/nginx/nginx.conf
LABEL org.opencontainers.image.source https://github.com/noah-witt/sfpd-log
