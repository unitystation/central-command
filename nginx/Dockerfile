FROM nginx:1.21-alpine

RUN rm /etc/nginx/conf.d/default.conf
ENV home=/home/website
RUN mkdir $home
RUN mkdir $home/statics
RUN mkdir $home/media
COPY nginx.conf /etc/nginx/conf.d