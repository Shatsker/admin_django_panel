FROM python:3.8.3-alpine

EXPOSE 8000/tcp

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app

RUN python admin_app/manage.py collectstatic --noinput
