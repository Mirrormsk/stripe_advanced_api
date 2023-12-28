FROM python:3.12-slim

ENV PYTHONDONTWRITEBYCODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION 1.7.1
WORKDIR /code

RUN #apt-get update && apt-get install -y gcc libjpeg-dev libpq-dev

RUN pip install --upgrade pip
RUN pip install poetry

COPY ./poetry.lock /code/poetry.lock
COPY ./pyproject.toml /code/pyproject.toml

RUN poetry  config virtualenvs.create false --local && poetry install
COPY . .

CMD ["poetry", "run", "python3", "manage.py", "runserver", "0.0.0.0:8000"]