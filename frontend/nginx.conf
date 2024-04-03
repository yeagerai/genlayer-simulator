gzip on;
gzip_disable "msie6";
gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript image/svg+xml;

server {
  listen 80 default_server;
  listen [::]:80 default_server;

  root /usr/share/nginx/html;

  index index.html;

  location ~ ^/(css|js)/ {
    # These assets include a digest in the filename, so they will never change
    expires max;
  }

  location ~* ^.+\.(html|htm)$ {
    # Very short caching time to ensure changes are immediately recognized
    expires 5m;
  }

  location / {
    try_files $uri $uri/ /index.html;
  }
}