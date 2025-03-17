# Build an egg of your project.

FROM python as build-stage

RUN pip install --no-cache-dir scrapyd-client

WORKDIR /workdir

COPY . .

RUN scrapyd-deploy --build-egg=myproject.egg

# Build the image.

FROM python:alpine

# Install Scrapy dependencies - and any others for your project.

RUN apk --no-cache add --virtual build-dependencies \
   gcc \
   musl-dev \
   libffi-dev \
   libressl-dev \
   libxml2-dev \
   libxslt-dev \
 && pip install --no-cache-dir \
   scrapyd \
 && apk del build-dependencies \
 && apk add \
   libressl \
   libxml2 \
   libxslt

# Mount two volumes for configuration and runtime.

VOLUME /etc/scrapyd/ /var/lib/scrapyd/

COPY ./scrapyd.conf /etc/scrapyd/

RUN mkdir -p /src/eggs/myproject

COPY --from=build-stage /workdir/myproject.egg /src/eggs/myproject/1.egg

EXPOSE 6800

ENTRYPOINT ["scrapyd", "--pidfile="]