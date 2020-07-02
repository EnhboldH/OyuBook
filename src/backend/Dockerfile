# Written: ByamB4
FROM python:3.6

RUN mkdir /app
WORKDIR /app

ADD . /app

ENV PYTHONNUNBUFFERED 1
ENV LANG C.UTF-8

ENV PORT=8000

RUN apt update && apt install -y --no-install-recommends \
    python3-setuptools \
    python3-pip \
    python3-dev \
    python3-venv \
    && \
  apt clean

RUN pipenv install --skip-lock --system --dev

EXPOSE 8888
CMD gunicorn oyucore.wsgi:application --bind 0.0.0.0:$PORT
