# 🚀 Python Telegram Bot Template

[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue?logo=python&logoColor=white)](https://python.org)
[![aiogram](https://img.shields.io/badge/aiogram-3.21-orange?logo=telegram&logoColor=white)](https://github.com/aiogram/aiogram)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red?logo=sqlite&logoColor=white)](https://www.sqlalchemy.org/)
[![Pydantic](https://img.shields.io/badge/Pydantic-2.11-darkred?logo=pydantic&logoColor=white)](https://docs.pydantic.dev/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

Современный, масштабируемый и готовый к продакшену шаблон (boilerplate) для разработки Telegram-ботов на Python. Создан на базе **aiogram v3** с фокусом на чистоту кода, расширяемость архитектуры и простоту поддержки.

Этот шаблон избавляет вас от рутинной настройки проекта и предоставляет готовую экосистему для быстрой разработки качественных ботов любой сложности.

---

## 🔥 Главные преимущества и особенности

### 1. ⚙️ Умная авторегистрация хэндлеров (Dynamic Routing)
Забудьте о ручном импорте и регистрации роутеров в `main.py`! Шаблон автоматически сканирует директорию `app/handlers` рекурсивно, находит все файлы с переменной `router` и подключает их к диспетчеру. 
* **Как это помогает:** Чтобы создать новый раздел бота, просто создайте `.py` файл в папке `handlers` и определите в нем `router = Router()`. Всё настроится автоматически!

### 2. 🛡️ Продвинутая защита от спама (Smart Throttling Middleware)
Встроенный механизм ограничения частоты запросов (Rate Limiting), использующий эффективный кэш `TTLCache`.
* Поддержка различных уровней задержки (`fast`, `slow`, `default`).
* Простейшая интеграция с хэндлерами через флаги: `@router.message(..., flags={'throttling_key': 'fast'})`.
* Автоматическая отправка предупреждений и уведомлений о разблокировке для удобства пользователя.

### 3. 🔌 Автоматическое управление сессиями БД (SQLAlchemy 2.0 & asyncpg)
Полностью асинхронный стек для работы с реляционными базами данных (PostgreSQL) с использованием SQLAlchemy 2.0.
* **Middleware-инъекция:** Сессия базы данных автоматически внедряется в параметры обработчика (`data["session"]`) при каждом входящем событии.
* **Опциональный запуск:** Базу данных можно полностью отключить в конфигурационном файле (`DB_IS_ENABLED=false`), и бот продолжит работать без неё. 

### 4. 📝 Строгая валидация конфигурации с Pydantic
Все настройки приложения загружаются из файла `.env` и валидируются с помощью `pydantic-settings`.
* Четкое разделение префиксов для бота, базы данных и платежей (`BOT_`, `DB_`, `PAYMENTS_`).
* Автоматическое преобразование типов данных (например, парсинг списка ID администраторов из JSON-строки).

### 5. 📂 Продуманная модульная структура
Код разделен по классическим канонам архитектуры чистых приложений: хэндлеры, фильтры, клавиатуры, middlewares, тексты и модели базы данных разложены по соответствующим пакетам.

---

## 📁 Архитектурная структура проекта

```text
null_bot/
├── app/                        # Исходный код приложения
│   ├── database/               # Модуль работы с БД
│   │   ├── models/             # SQLAlchemy модели (ORM)
│   │   │   ├── base.py         # Базовый декларативный класс
│   │   │   └── __init__.py
│   │   ├── engine.py           # Инициализация асинхронного движка и сессий
│   │   └── __init__.py
│   ├── filters/                # Кастомные aiogram фильтры (например, IsAdmin)
│   ├── handlers/               # Обработчики команд и сообщений (автоимпортируемые)
│   │   ├── admin/              # Панель администратора
│   │   └── start.py            # Обработчик стартового меню
│   ├── keyboards/              # Reply и Inline клавиатуры
│   ├── middlewares/            # Промежуточные слои (throttling, sessions и др.)
│   ├── texts/                  # Текстовые константы и локализация
│   ├── commands.py             # Определение команд меню бота
│   └── config.py               # Конфигурация и валидация окружения (Pydantic)
├── example.env                 # Шаблон для файла настроек .env
├── main.py                     # Точка входа в приложение
└── requirements.txt            # Зависимости проекта
```

---

## 🛠️ Разбор ключевых фич (Deep Dive)

### Динамическое подключение роутеров
Вместо ручного прописывания десятков роутеров в `main.py`, в шаблоне реализован автоимпорт:

```python
# app/handlers/__init__.py
package_dir = Path(__file__).parent
for path in package_dir.rglob("*.py"):
    if path.name == "__init__.py":
        continue
    
    relative_path = path.relative_to(package_dir.parent)
    module_parts = relative_path.with_suffix("").parts
    module_name = ".".join(module_parts)

    module = import_module(f".{module_name}", package="app")
    router = getattr(module, "router", None)
    if router:
        routers.append(router)
```

### Использование антиспама в хэндлерах
Для включения троттлинга на хэндлер достаточно указать флаг:

```python
@router.message(Command("search"), flags={"throttling_key": "fast"})
async def search_handler(message: Message):
    await message.reply("Выполняю поиск...")
```

### Внедрение сессии БД в хэндлеры
Middleware автоматически передает сессию SQLAlchemy прямо в аргументы функции обработчика:

```python
@router.message(Command("profile"))
async def show_profile(message: Message, session: AsyncSession):
    # Работа с сессией происходит асинхронно и безопасно
    user = await session.get(User, message.from_user.id)
    await message.reply(f"Ваш баланс: {user.balance}")
```

---

## 🚀 Быстрый старт

### 1. Клонирование репозитория и установка зависимостей
```bash
git clone https://github.com/vita-ctrl/null_bot.git
cd null_bot
```
Создайте виртуальное окружение и установите библиотеки:
```bash
python -m venv venv
source venv/bin/activate  # Для Linux/macOS
# venv\Scripts\activate  # Для Windows

pip install -r requirements.txt
```

### 2. Настройка окружения
Создайте файл `.env` на основе шаблона `example.env`:
```bash
cp example.env .env
```
Заполните переменные конфигурации:
```env
BOT_TOKEN=1234567890:ABCdefGhIJKlmNoPQRsTUVwxyZ  # Токен от BotFather
BOT_ADMINS=[111222333, 444555666]                # ID администраторов через запятую

DB_IS_ENABLED=true                               # Переключите в false, если БД не нужна
DB_HOST=localhost
DB_PORT=5432
DB_NAME=bot_db
DB_USER=postgres
DB_PASSWORD=secret_password

PAYMENTS_TOKEN=                                  # Токен провайдера платежей (опционально)
```

### 3. Запуск бота
```bash
python main.py
```
