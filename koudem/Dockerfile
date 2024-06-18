FROM python:3.10.4-alpine3.15

WORKDIR /app


RUN set -eux; \
    apk add --no


COPY ./requirements.txt ./

RUN pip install -r requirements

COPY ./ ./

CMD ["python","manage.py","runserver","0.0.0.0:8000"]