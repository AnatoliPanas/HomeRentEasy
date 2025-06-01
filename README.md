# HomeRentEasy

## О проекте

**HomeRentEasy** — полнофункциональный back-end для системы аренды жилья на Django.  
Проект поддерживает работу с объявлениями, бронированиями, отзывами, ролями пользователей, фильтрацией, JWT-аутентификацией, REST API, тестами и развертыванием через Docker/MySQL.

---

## 1. Быстрый старт (Windows + PyCharm)

### 1.1. Клонируйте репозиторий

```sh
git clone <your_repo_url>
cd HomeRentEasy
```

### 1.2. Создайте виртуальное окружение (venv)

```sh
python -m venv venv
venv\Scripts\activate
```

### 1.3. Установите зависимости

```sh
pip install -r requirements.txt
```

### 1.4. Настройте переменные окружения

- Скопируйте `.env.example` в `.env` и заполните своими значениями:

```sh
copy .env.example .env
```

- Проверьте/установите параметры SECRET_KEY, DEBUG, ALLOWED_HOSTS, MYSQL и данные базы.

---

## 2. Запуск с MySQL через Docker Compose

### 2.1. Проверьте настройки .env

- Убедитесь, что в `.env` указано:
  ```
  MYSQL=True
  MYSQL_USER=...
  MYSQL_PASSWORD=...
  MYSQL_DB=...
  MYSQL_ROOT_PASSWORD=...
  ```

### 2.2. Запустите контейнер MySQL

```sh
docker-compose up -d
```

- Убедитесь, что контейнер mysql поднялся (`docker ps`).

### 2.3. Примените миграции и запустите сервер

```sh
python manage.py migrate
python manage.py runserver
```

---

## 3. Документация API

- Swagger: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
- Redoc: [http://localhost:8000/redoc/](http://localhost:8000/redoc/)

---

## 4. Переменные окружения (.env / .env.example)

- `SECRET_KEY` — секретный ключ Django
- `DEBUG` — режим отладки (True/False)
- `ALLOWED_HOSTS` — список хостов через запятую
- `MYSQL` — использовать ли MySQL (True/False)
- `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DB`, `MYSQL_ROOT_PASSWORD` — параметры БД
- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` — для деплоя на AWS (по необходимости)

---

## 5. Работа с виртуальным окружением в PyCharm

1. В PyCharm:  
   `File → Settings… → Project: HomeRentEasy → Python Interpreter → Add Interpreter → Existing environment → .../venv/Scripts/python.exe`
2. Запускать manage.py/runserver можно прямо из IDE.

---

## 6. Тестирование

```sh
python manage.py test
```

---

## 7. Альтернативы запуска

- Для быстрого старта используйте SQLite (в .env: `MYSQL=False`)
- Для продакшна — MySQL через Docker Compose

---

## 8. Деплой на AWS EC2

1. Разверните проект на сервере, установите Docker и docker-compose.
2. Настройте переменные окружения (`.env`).
3. Запустите `docker-compose up -d` для БД, затем миграции и сервер.
4. Настройте Gunicorn/Nginx при необходимости.

---

## 9. Пример .env.example

```dotenv
SECRET_KEY=your_secret_key
ALLOWED_HOSTS=127.0.0.1,localhost
DEBUG=True

MYSQL=True
MYSQL_USER=...
MYSQL_PASSWORD=...
MYSQL_DB=...
MYSQL_ROOT_PASSWORD=...

# AWS_ACCESS_KEY_ID=your_aws_key
# AWS_SECRET_ACCESS_KEY=your_aws_secret
```

---

## 10. Структура проекта (основные директории)

```
HomeRentEasy/
├── applications/
│   ├── users/
│   ├── rent/
│   ├── bookings/
│   └── reviews/
├── HomeRentEasy/
├── requirements.txt
├── docker-compose.yaml
├── manage.py
├── .env.example
└── README.md
```

---

## 11. Обратная связь

По вопросам пишите [контакту из Swagger](mailto:net@net.net).
