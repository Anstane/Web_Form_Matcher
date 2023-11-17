FROM python:3.11-slim

RUN pip install poetry

WORKDIR /app/

COPY pyproject.toml poetry.lock /app/

RUN poetry install --no-root --no-dev

COPY . /app/

EXPOSE 5000

CMD ["poetry", "run", "flask", "run", "--host", "0.0.0.0"]
