# pull official base image
FROM python:3.7-alpine AS builder

RUN apk add \
    build-base \
    python3 \
    python3-dev \
    # wget dependency
    openssl \
    # dev dependencies
    bash \
    git \
    py3-pip \
    sudo \
    # Pillow dependencies
    freetype-dev \
    fribidi-dev \
    harfbuzz-dev \
    jpeg-dev \
    lcms2-dev \
    openjpeg-dev \
    tcl-dev \
    tiff-dev \
    tk-dev \
    zlib-dev

RUN pip install --upgrade pip

RUN pip install Pillow


FROM builder
# set work directory
ADD . /
WORKDIR /
ENV PYTHONPATH /

ENV PYTHONPATH /
CMD ["/main.py"]
# CMD ["bash", "test"]
