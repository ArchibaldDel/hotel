
# Hotel Booking API

Простой сервис для управления **номерами отелей** и **бронированиями**.
Реализован на **Django + DRF**, используется **PostgreSQL** и запускается через **Docker Compose**.
Проект разработан как учебное задание, но структура приближена к реальному продакшн-приложению.

---

## Функционал

### Rooms (Номера отеля)

* **Создание номера**: POST `/rooms/`
  Принимает `description` (текст) и `price_per_night` (Decimal).
  Возвращает ID номера.
* **Список номеров**: GET `/rooms/list/`
  Поддерживает сортировку по цене и дате добавления (`?ordering=price_per_night` / `-price_per_night`, `created_at`).
* **Удаление номера**: DELETE `/rooms/{id}/`
  Удаляет номер и все связанные брони.

### Bookings (Бронирования)

* **Создание брони**: POST `/bookings/`
  Принимает `room`, `date_start`, `date_end`.
  Проверка занятости номера не реализована (можно добавить как улучшение).
* **Список броней номера**: GET `/bookings/list/?room_id={id}`
  Сортировка по дате начала.
* **Удаление брони**: DELETE `/bookings/{id}/`.

---

## Технологии

* Python 3.11
* Django 5 + Django REST Framework
* PostgreSQL 16
* Poetry (менеджер зависимостей)
* Docker, Docker Compose
* Pytest (юнит- и API-тесты)
* Ruff (линтер и форматтер)

---

## Установка и запуск

### 1. Клонирование проекта

```bash
git clone https://github.com/<your-username>/hotel-api.git
cd hotel-api
```

### 2. Запуск через Docker

```bash
docker compose up --build
```

После запуска API будет доступно на
👉 [http://localhost:9000](http://localhost:9000)

Проверить health-чек:

```bash
curl http://localhost:9000/health
# {"service": "hotel-booking-api", "status": "healthy"}
```

### 3. Запуск локально (через Poetry)

Требуется установленный **PostgreSQL**.

```bash
poetry install
poetry run python manage.py migrate
poetry run python manage.py runserver 0.0.0.0:9000
```

---

## Переменные окружения

Создайте файл `.env` в корне проекта:

```env
POSTGRES_DB=hotel_db
POSTGRES_USER=hotel_user
POSTGRES_PASSWORD=hotel_pass
DB_HOST=db
DB_PORT=5432
DJANGO_SECRET_KEY=unsafe-dev-key
DEBUG=1
ALLOWED_HOSTS=*
```

---

## Тестирование

### Запуск тестов

```bash
docker compose run --rm web pytest -v
```

### Покрытие кода

```bash
docker compose run --rm web pytest --cov=hotels
```

### Линтер

```bash
docker compose run --rm web ruff check .
```

Авто-фикс:

```bash
docker compose run --rm web ruff check . --fix
```

---

## Структура проекта

```
hotel-api/
│── config/              # Django config (settings, urls, wsgi)
│── hotels/              # Основное приложение
│   ├── models.py        # Room, Booking
│   ├── views.py         # APIView / GenericAPIView
│   ├── serializers.py   # DRF сериализаторы
│   ├── urls.py          # эндпоинты
│   └── tests/           # тесты (unit, api, e2e)
│── docker-compose.yml   # Docker Compose
│── Dockerfile           # образ web-сервиса
│── pyproject.toml       # poetry зависимости
│── README.md            # документация
└── .gitignore
```

---

## Принятые решения

* Использован Django + DRF для скорости разработки (вместо Go/PHP).
* Для хранения данных выбрана PostgreSQL.
* Миграции используются стандартные Django (вместо raw SQL).
* Добавлены автотесты (unit, API, e2e).
* Кодстайл и линтер: Ruff.
* Запуск через Docker Compose для удобства.

