FROM nginx:1.24.0-alpine

COPY ./* /etc/nginx/
#COPY ./default.conf /etc/nginx/conf.d/default.conf

USER root

RUN apk add --no-cache openssl bash
RUN chmod +x /run.sh

VOLUME /vol/static
VOLUME /vol/www

CMD ["/run.sh"]
