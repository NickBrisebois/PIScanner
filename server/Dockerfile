FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./
RUN poetry install --only=main --no-dev

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
