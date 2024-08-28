FROM nginx

COPY . /usr/share/nginx/

COPY nginx/certificate/nginx-selfsigned.crt /etc/nginx/ssl/nginx-selfsigned.crt
COPY nginx/certificate/nginx-selfsigned.key /etc/nginx/ssl/nginx-selfsigned.key

COPY nginx/config/nginx.conf /etc/nginx/nginx.conf