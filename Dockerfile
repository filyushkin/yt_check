FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Установка зависимостей
COPY uv.lock .
COPY pyproject.toml .

# Копирование проекта
COPY . .

RUN uv sync

# Команда для запуска, будет переопределена в docker-compose
CMD ["uv", "run", "manage.py", "runserver", "0.0.0.0:8000"]
