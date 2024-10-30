FROM python:3.12-slim

WORKDIR /cloudflare_dynamic_ip_updater

COPY requirements.txt requirements.txt
RUN python3 -m pip install -r requirements.txt

RUN python3 -m pip install 'opentelemetry-distro[otlp]'
RUN opentelemetry-bootstrap -a install

COPY . .

RUN mkdir /var/log/cloudflare_dynamic_ip_updater
ENV LOGS_DIR /var/log/cloudflare_dynamic_ip_updater

ENTRYPOINT [ "python3" ]
CMD [ "main.py" ]