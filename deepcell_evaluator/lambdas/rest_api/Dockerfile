ARG FUNCTION_DIR="/home/lambda/"
ARG RUNTIME_VERSION="3.9"
ARG DISTRO_VERSION="3.12"
ARG SERVERLESS_TAG="1.7.6"

FROM python:${RUNTIME_VERSION}-alpine${DISTRO_VERSION} AS python-alpine

RUN apk add --no-cache \
    libstdc++

FROM python-alpine AS build-image

RUN apk add --no-cache \
    build-base \
    libtool \
    autoconf \
    automake \
    libexecinfo-dev \
    make \
    cmake \
    libcurl \
    git

ARG FUNCTION_DIR
ARG RUNTIME_VERSION
ARG SERVERLESS_TAG

RUN mkdir -p ${FUNCTION_DIR}

RUN python${RUNTIME_VERSION} -m pip install awslambdaric --target ${FUNCTION_DIR}

COPY . ${FUNCTION_DIR}.
COPY ./utils ${FUNCTION_DIR}utils

RUN python${RUNTIME_VERSION} -m pip install -r ${FUNCTION_DIR}/requirements.txt --target ${FUNCTION_DIR}

RUN git config --global advice.detachedHead false
RUN git clone https://github.com/logandk/serverless-wsgi --branch ${SERVERLESS_TAG} ${FUNCTION_DIR}serverless-wsgi
RUN cp ${FUNCTION_DIR}serverless-wsgi/wsgi_handler.py ${FUNCTION_DIR}wsgi_handler.py && cp ${FUNCTION_DIR}serverless-wsgi/serverless_wsgi.py ${FUNCTION_DIR}serverless_wsgi.py

FROM python-alpine

ARG FUNCTION_DIR

WORKDIR ${FUNCTION_DIR}

COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}

ADD https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie /usr/bin/aws-lambda-rie
RUN chmod 755 /usr/bin/aws-lambda-rie
COPY entry.sh /
RUN chmod +x entry.sh

ENTRYPOINT [ "./entry.sh" ]
CMD [ "wsgi_handler.handler" ]