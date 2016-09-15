FROM nginx:alpine
COPY confd /confd

RUN apk add --update bash && \
    chmod +x /confd

COPY nginx.conf.tmpl /etc/confd/templates/nginx.conf.tmpl
COPY nginx.conf.toml /etc/confd/conf.d/nginx.conf.toml

