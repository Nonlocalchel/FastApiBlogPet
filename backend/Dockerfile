FROM python:3.12.2-alpine

ENV PYTHONDONTWRITEBITECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk add gcc musl-dev libffi-dev
RUN pip install --upgrade pip \
    && pip install poetry


ENV HOME=/home/app
ENV APP_HOME=/home/app/backend

RUN mkdir $HOME && mkdir $APP_HOME
WORKDIR $APP_HOME
COPY /backend $APP_HOME
COPY .env $APP_HOME/.env.prod

COPY /backend/start_backend.sh /usr/local/bin/start_backend.sh
RUN chmod +x /usr/local/bin/start_backend.sh

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

RUN adduser --disabled-password task-user \
    && chown -R task-user:task-user $APP_HOME \
    && chown -R task-user:task-user $HOME/.config/pypoetry/config.toml

USER task-user

ENTRYPOINT ["start_backend.sh"]