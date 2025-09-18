# Развертывание Telegram бота в продакшене

Это руководство поможет вам развернуть Telegram бота на сервере с nginx+SSL.

## 📋 Требования

- Ubuntu/Debian сервер с nginx
- Python 3.8+
- SSL сертификат (Let's Encrypt рекомендуется)
- Домен с настроенным DNS

## 🚀 Быстрый деплой

### 1. Подготовка сервера

```bash
# Обновляем систему
sudo apt update && sudo apt upgrade -y

# Устанавливаем необходимые пакеты
sudo apt install -y python3 python3-pip python3-venv nginx certbot python3-certbot-nginx

# Создаем пользователя для бота
sudo useradd -r -s /bin/false telegram_bot
```

### 2. Клонирование и настройка

```bash
# Клонируем проект (или копируем файлы)
cd /opt
sudo git clone <your-repo> telegram_bot
# или
sudo mkdir telegram_bot
# Скопируйте все файлы проекта в /opt/telegram_bot

# Устанавливаем права
sudo chown -R www-data:www-data /opt/telegram_bot
sudo chmod +x /opt/telegram_bot/deploy.sh
sudo chmod +x /opt/telegram_bot/bot_manager.sh
```

### 3. Настройка переменных окружения

```bash
cd /opt/telegram_bot
sudo cp env_production_example .env
sudo nano .env
```

Заполните все необходимые переменные:
- `BOT_TOKEN` - токен вашего бота от @BotFather
- `ADMIN_CHAT_ID` - ваш Telegram ID
- `WEBHOOK_URL` - https://yourdomain.com/webhook/telegram
- `PRODAMUS_SHOP_ID` и `PRODAMUS_SECRET_KEY` - данные от Продамус
- `CHANNEL_ID` и `CHANNEL_USERNAME` - данные вашего канала

### 4. Настройка SSL сертификата

```bash
# Получаем SSL сертификат от Let's Encrypt
sudo certbot --nginx -d yourdomain.com

# Автообновление сертификатов
sudo crontab -e
# Добавьте строку:
# 0 12 * * * /usr/bin/certbot renew --quiet
```

### 5. Настройка nginx

```bash
# Копируем конфигурацию nginx
sudo cp nginx_config.conf /etc/nginx/sites-available/telegram_bot

# Редактируем домен в конфигурации
sudo nano /etc/nginx/sites-available/telegram_bot
# Замените yourdomain.com на ваш реальный домен

# Активируем сайт
sudo ln -s /etc/nginx/sites-available/telegram_bot /etc/nginx/sites-enabled/

# Проверяем конфигурацию
sudo nginx -t

# Перезагружаем nginx
sudo systemctl reload nginx
```

### 6. Запуск бота

```bash
cd /opt/telegram_bot
sudo ./deploy.sh
```

## 🔧 Управление ботом

Используйте скрипт `bot_manager.sh` для управления ботом:

```bash
# Запустить бота
sudo ./bot_manager.sh start

# Остановить бота
sudo ./bot_manager.sh stop

# Перезапустить бота
sudo ./bot_manager.sh restart

# Показать статус
sudo ./bot_manager.sh status

# Показать логи
sudo ./bot_manager.sh logs

# Проверить здоровье
sudo ./bot_manager.sh health

# Обновить код бота
sudo ./bot_manager.sh update

# Создать бэкап БД
sudo ./bot_manager.sh backup
```

## 📊 Мониторинг

### Health Check
```bash
curl https://yourdomain.com/health
```

### Статус бота
```bash
curl https://yourdomain.com/status
```

### Логи в реальном времени
```bash
sudo journalctl -u telegram_bot -f
```

## 🔒 Безопасность

### Firewall
```bash
# Настраиваем UFW
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

### Обновления
```bash
# Автоматические обновления безопасности
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

## 📁 Структура файлов

```
/opt/telegram_bot/
├── bot_webhook.py          # Основной файл бота с webhook
├── admin_panel.py          # Админ-панель
├── channel_manager.py      # Управление каналом
├── config.py              # Конфигурация
├── database.py            # Работа с БД
├── prodamus.py            # Интеграция с Продамус
├── scheduler.py           # Планировщик задач
├── init_db.py             # Инициализация БД
├── requirements.txt       # Зависимости Python
├── .env                   # Переменные окружения
├── women_club.db          # База данных SQLite
├── logs/                  # Логи приложения
├── backups/               # Бэкапы БД
├── ssl/                   # SSL сертификаты
├── deploy.sh              # Скрипт деплоя
├── bot_manager.sh         # Управление ботом
├── nginx_config.conf      # Конфигурация nginx
├── telegram_bot.service   # Systemd сервис
└── env_production_example # Пример .env
```

## 🚨 Устранение неполадок

### Бот не запускается
```bash
# Проверяем статус
sudo systemctl status telegram_bot

# Смотрим логи
sudo journalctl -u telegram_bot -n 50

# Проверяем права доступа
sudo chown -R www-data:www-data /opt/telegram_bot
```

### Webhook не работает
```bash
# Проверяем nginx
sudo nginx -t
sudo systemctl status nginx

# Проверяем SSL сертификат
sudo certbot certificates

# Тестируем webhook локально
curl -X POST http://localhost:5000/health
```

### Проблемы с базой данных
```bash
# Проверяем права на БД
ls -la /opt/telegram_bot/women_club.db

# Создаем новый бэкап
sudo ./bot_manager.sh backup

# Восстанавливаем из бэкапа
sudo cp /opt/telegram_bot/backups/women_club_YYYYMMDD_HHMMSS.db /opt/telegram_bot/women_club.db
```

## 📈 Масштабирование

Для высоконагруженных проектов рассмотрите:

1. **PostgreSQL вместо SQLite**
2. **Redis для кэширования**
3. **Docker контейнеры**
4. **Load balancer**
5. **Мониторинг (Prometheus + Grafana)**

## 🔄 Обновления

Для обновления бота:

```bash
# Останавливаем бота
sudo ./bot_manager.sh stop

# Создаем бэкап
sudo ./bot_manager.sh backup

# Обновляем код
sudo git pull origin main
# или копируете новые файлы

# Запускаем обновленную версию
sudo ./bot_manager.sh update
```

## 📞 Поддержка

При возникновении проблем:

1. Проверьте логи: `sudo ./bot_manager.sh logs`
2. Проверьте здоровье: `sudo ./bot_manager.sh health`
3. Проверьте статус: `sudo ./bot_manager.sh status`
4. Создайте бэкап: `sudo ./bot_manager.sh backup`
