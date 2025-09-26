# Telegram Bot для Женского Клуба

## 📁 Структура проекта

```
tg_psy/
├── 📁 tests/                    # Тестовые файлы
│   ├── test_contact_verification.py
│   ├── test_webhook.py
│   ├── test_prodamus_webhook.py
│   ├── test_payment_check.py
│   └── ...
├── 📁 docs/                     # Документация
│   ├── README.md
│   ├── DEPLOYMENT_READY_REPORT.md
│   ├── PAYMENT_GUIDE.md
│   └── ...
├── 📁 scripts/                  # Скрипты развертывания
│   ├── deploy_linux.sh
│   ├── setup_ssl_nginx.sh
│   ├── init_contact_system.sh
│   └── ...
├── 📁 configs/                  # Конфигурационные файлы
│   ├── nginx_ssl_config.conf
│   ├── telegram_bot.service
│   └── ...
├── 📁 backups/                  # Резервные копии
│   ├── *.backup
│   ├── *_fixed.py
│   └── ...
├── 🤖 Основные файлы бота
│   ├── bot.py                   # Основной файл бота
│   ├── webhook.py               # Webhook сервер
│   ├── database.py              # Работа с базой данных
│   ├── prodamus.py              # Интеграция с Prodamus
│   ├── config.py                # Конфигурация
│   └── main_with_pagekite.py    # Запуск с PageKite
└── 📄 Другие файлы
    ├── requirements.txt
    ├── .env
    └── ...
```

## 🚀 Быстрый старт

### 1. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 2. Настройка конфигурации
```bash
cp .env.example .env
# Отредактируйте .env файл
```

### 3. Инициализация базы данных
```bash
python3 init_database.py
```

### 4. Запуск системы
```bash
# Запуск с PageKite
python3 main_with_pagekite.py

# Или запуск отдельных компонентов
python3 webhook.py &
python3 bot.py
```

## 🧪 Тестирование

```bash
# Запуск всех тестов
python3 tests/test_contact_verification.py

# Проверка webhook
python3 tests/test_webhook.py

# Проверка платежей
python3 tests/test_payment_check.py
```

## 📚 Документация

- [Руководство по развертыванию](docs/DEPLOYMENT_READY_REPORT.md)
- [Настройка платежей](docs/PAYMENT_GUIDE.md)
- [Настройка SSL](docs/SSL_NGINX_SETUP_REPORT.md)
- [Настройка PageKite](docs/PAGKITE_SETUP_INSTRUCTIONS.md)

## 🔧 Скрипты

- `scripts/deploy_linux.sh` - Развертывание на Linux
- `scripts/setup_ssl_nginx.sh` - Настройка SSL и Nginx
- `scripts/init_contact_system.sh` - Инициализация системы контактов

## 📋 Основные функции

- ✅ Сбор контактных данных (телефон, email)
- ✅ Интеграция с Prodamus для платежей
- ✅ Автоматическая активация подписок
- ✅ Webhook для обработки платежей
- ✅ Админ-панель
- ✅ Управление каналами

## ⚙️ Конфигурация

Основные настройки в `config.py`:
- `BOT_TOKEN` - Токен Telegram бота
- `PRODAMUS_SHOP_ID` - ID магазина Prodamus
- `PRODAMUS_SECRET_KEY` - Секретный ключ Prodamus
- `FLASK_PORT` - Порт webhook сервера (3000)

## 🔒 Безопасность

- Проверка подписи webhook (временно отключена для тестирования)
- Валидация контактных данных
- Безопасное хранение конфигурации

## 📞 Поддержка

При возникновении проблем:
1. Проверьте логи: `tail -f webhook.log`
2. Запустите тесты: `python3 tests/test_contact_verification.py`
3. Проверьте конфигурацию: `python3 check_config.py`
