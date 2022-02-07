FROM nginx:1.21-alpine

RUN rm /etc/nginx/conf.d/default.conf
RUN mkdir /home/website
RUN mkdir /home/website/statics
RUN mkdir /home/website/media
COPY nginx.conf /etc/nginx/conf.d