#FROM python:3.12.2-alpine
#
#EXPOSE 8000
#
#WORKDIR /code
#
#RUN pip install --upgrade pip
#RUN apk add gcc musl-dev libffi-dev
#RUN pip install poetry
#
#COPY . /code
#
#RUN poetry config virtualenvs.create false \
#    && poetry install --no-interaction --no-ansi
#
#CMD ["poetry", "python", "main.py"]
FROM python:3.12.2-alpine

ENV PYTHONDONTWRITEBITECODE 1
ENV PYTHONUNBUFFERED 1


RUN pip install --upgrade pip
RUN apk add gcc musl-dev libffi-dev
RUN pip install poetry


ENV HOME=/home/app
ENV APP_HOME=/home/app/backend

RUN mkdir $HOME && mkdir $APP_HOME
WORKDIR $APP_HOME
COPY . $APP_HOME

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

RUN adduser --disabled-password task-user \
    && chown -R task-user:task-user $APP_HOME

USER task-user

CMD ["python", "main.py"]