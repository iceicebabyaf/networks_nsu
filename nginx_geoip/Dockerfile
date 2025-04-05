FROM nginx:1.27.4

RUN apt update && apt install -y \
    build-essential curl wget unzip libpcre3 libpcre3-dev zlib1g zlib1g-dev libssl-dev \
    libmaxminddb-dev git ca-certificates && \
    git clone --depth=1 https://github.com/leev/ngx_http_geoip2_module.git /usr/src/ngx_http_geoip2_module && \
    wget http://nginx.org/download/nginx-1.27.4.tar.gz -P /usr/src && \
    cd /usr/src && \
    tar -xvzf nginx-1.27.4.tar.gz && \
    cd nginx-1.27.4 && \
    ./configure --with-compat --add-dynamic-module=../ngx_http_geoip2_module && \
    make modules && \
    cp objs/ngx_http_geoip2_module.so /etc/nginx/modules/ && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY nginx.conf /etc/nginx/nginx.conf
COPY ./GeoLite2-Country.mmdb /usr/share/GeoIP/GeoLite2-Country.mmdb

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
