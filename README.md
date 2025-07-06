# Book Library API

Учебный асинхронный REST-сервис на **FastAPI**. Предоставляет CRUD-эндпоинты для двух сущностей — **книг** и **продавцов**.

---

## Возможности

- **FastAPI + Uvicorn** — высокопроизводительный ASGI-сервер  
- **SQLAlchemy 2.0 (async)** — асинхронный доступ к PostgreSQL  
- **Pydantic v2** — строгая валидация входящих/исходящих данных  
- Автодокументация Swagger UI и ReDoc (`/docs`, `/redoc`)  
- Интеграционные и unit-тесты на **pytest**  
- Готовый `docker-compose` для PostgreSQL (две БД: prod и test)  
- Конфигурация через переменные окружения (`.env.example`)  

---

## Быстрый старт

> Требования: **Python ≥ 3.12** и **Docker**.

```bash
# Клонируем проект
git clone https://github.com/<YOUR_GH_LOGIN>/fast_api_shad.git
cd fast_api_shad

# Создаём .env на основе примера
cp .env.example .env              # поправьте значения при необходимости

# Поднимаем PostgreSQL
docker compose up -d              # база слушает 127.0.0.1:5445

# Устанавливаем зависимости
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt   # либо poetry install

# Запускаем приложение
uvicorn src.main:app --reload --port 8000
````

После старта:

* **Swagger UI** — [http://localhost:8000/docs](http://localhost:8000/docs)
* **ReDoc** — [http://localhost:8000/redoc](http://localhost:8000/redoc)

Таблицы создаются автоматически при запуске.

## Примеры запросов

```http
### Создать продавца
POST http://localhost:8000/api/v1/sellers
Content-Type: application/json

{
  "name": "O'Reilly Media",
  "country": "USA",
  "city": "Sebastopol"
}

### Создать книгу
POST http://localhost:8000/api/v1/books
Content-Type: application/json

{
  "title": "Designing Data-Intensive Applications",
  "year": 2017,
  "seller_id": 1
}

### Получить список книг
GET http://localhost:8000/api/v1/books
```

Файлы `api_tests_*.http` можно открыть расширением **REST Client** в VS Code и отправлять запросы прямо из редактора.

## Структура каталогов

```
.
├── docker/                 # инфраструктура
│   └── postgres/
├── docker-compose.yml
├── requirements.txt
└── src/
    ├── configurations/     # настройки и подключение к БД
    ├── models/             # ORM-модели SQLAlchemy
    ├── schemas/            # Pydantic-DTO
    ├── routers/            # версионированные эндпоинты
    ├── tests/              # pytest-тесты
    └── main.py             # точка входа FastAPI
```

## Тестирование

```bash
pytest -q               # все тесты
pytest -k books         # выборочно
```

Интеграционные тесты используют отдельную БД `fastapi_project_test_db`, создаваемую через Docker-инициализатор (`docker/postgres/create_databases.sql`).

