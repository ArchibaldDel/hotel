FROM python:3.11-slim

# Ускоряем работу Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/root/.local/bin:$PATH"

WORKDIR /app

# --- Системные пакеты ---
# gcc и libpq-dev нужны для сборки psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev curl \
 && rm -rf /var/lib/apt/lists/*

# --- Устанавливаем Poetry ---
RUN pip install --no-cache-dir poetry \
 && poetry config virtualenvs.create false \
 && poetry config cache-dir /tmp/poetry_cache

# --- Устанавливаем зависимости (кэшируем слои) ---
COPY pyproject.toml poetry.lock* /app/
RUN poetry install --no-root --no-interaction --no-ansi

# --- Копируем проект ---
COPY . /app

# --- Команда запуска ---
CMD ["poetry", "run", "gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:9000"]
