FROM python:3.12-alpine

LABEL maintainer="mihai@developerakademie.com"
LABEL version="1.0"
LABEL description="Python 3.14.0a7 Alpine 3.21"

WORKDIR /app

RUN apk update && \
    apk add --no-cache --upgrade bash && \
    apk add --no-cache postgresql-client ffmpeg && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY ./app .

COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

EXPOSE 8000

ENTRYPOINT [ "/entrypoint.sh" ]
