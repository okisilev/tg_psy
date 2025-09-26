# Настройка продакшена - пошаговая инструкция

## 🎯 Что было создано для продакшена:

### 1. **bot_webhook.py** - Основной файл бота с поддержкой webhook
- Flask сервер для обработки webhook от Telegram и Продамус
- Асинхронная обработка обновлений через очередь
- Интеграция со всеми компонентами бота

### 2. **nginx_config.conf** - Конфигурация nginx
- Проксирование webhook запросов на Flask приложение
- SSL терминация
- Health check endpoints

### 3. **telegram_bot.service** - Systemd сервис
- Автозапуск бота при загрузке сервера
- Автоматический перезапуск при сбоях
- Безопасность и ограничения ресурсов

### 4. **deploy.sh** - Скрипт автоматического деплоя
- Установка зависимостей
- Настройка сервисов
- Инициализация базы данных

### 5. **bot_manager.sh** - Управление ботом
- Запуск/остановка/перезапуск
- Просмотр логов и статуса
- Обновление кода
- Бэкапы базы данных

### 6. **env_production_example** - Пример переменных окружения
- Все необходимые настройки для продакшена

## 🚀 Пошаговая настройка на сервере:

### Шаг 1: Подготовка сервера
```bash
# Подключитесь к серверу по SSH
ssh user@your-server.com

# Обновите систему
sudo apt update && sudo apt upgrade -y

# Установите необходимые пакеты
sudo apt install -y python3 python3-pip python3-venv nginx certbot python3-certbot-nginx
```

### Шаг 2: Загрузка файлов на сервер
```bash
# Создайте директорию для бота
sudo mkdir -p /opt/telegram_bot
sudo chown -R www-data:www-data /opt/telegram_bot

# Загрузите все файлы проекта на сервер
# Можно использовать scp, rsync или git clone
```

### Шаг 3: Настройка переменных окружения
```bash
cd /opt/telegram_bot
sudo cp env_production_example .env
sudo nano .env
```

**Заполните .env файл:**
```bash
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
ADMIN_CHAT_ID=123456789
WEBHOOK_URL=https://--help/webhook/telegram
PRODAMUS_SHOP_ID=your_shop_id
PRODAMUS_SECRET_KEY=your_secret_key
CHANNEL_ID=-1001234567890
CHANNEL_USERNAME=@your_channel
```

### Шаг 4: Настройка SSL сертификата
```bash
# Получите SSL сертификат от Let's Encrypt
sudo certbot --nginx -d --help

# Настройте автообновление
sudo crontab -e
# Добавьте строку:
# 0 12 * * * /usr/bin/certbot renew --quiet
```

### Шаг 5: Настройка nginx
```bash
# Скопируйте конфигурацию nginx
sudo cp nginx_config.conf /etc/nginx/sites-available/telegram_bot

# Отредактируйте домен в конфигурации
sudo nano /etc/nginx/sites-available/telegram_bot
# Замените --help на ваш реальный домен

# Активируйте сайт
sudo ln -s /etc/nginx/sites-available/telegram_bot /etc/nginx/sites-enabled/

# Проверьте конфигурацию
sudo nginx -t

# Перезагрузите nginx
sudo systemctl reload nginx
```

### Шаг 6: Запуск бота
```bash
cd /opt/telegram_bot

# Сделайте скрипты исполняемыми
sudo chmod +x deploy.sh bot_manager.sh

# Запустите деплой
sudo ./deploy.sh
```

### Шаг 7: Проверка работы
```bash
# Проверьте статус бота
sudo ./bot_manager.sh status

# Проверьте здоровье
sudo ./bot_manager.sh health

# Проверьте webhook
curl https://--help/health
```

## 🔧 Управление ботом:

```bash
# Запуск
sudo ./bot_manager.sh start

# Остановка
sudo ./bot_manager.sh stop

# Перезапуск
sudo ./bot_manager.sh restart

# Статус
sudo ./bot_manager.sh status

# Логи
sudo ./bot_manager.sh logs

# Обновление кода
sudo ./bot_manager.sh update

# Бэкап БД
sudo ./bot_manager.sh backup
```

## 🚨 Важные моменты:

1. **Домен**: Убедитесь, что ваш домен указывает на IP сервера
2. **SSL**: Обязательно настройте SSL сертификат
3. **Firewall**: Откройте порты 80 и 443
4. **Бэкапы**: Регулярно создавайте бэкапы базы данных
5. **Мониторинг**: Настройте мониторинг логов

## 📊 Мониторинг:

- **Health check**: `https://--help/health`
- **Статус бота**: `https://--help/status`
- **Логи**: `sudo journalctl -u telegram_bot -f`

## 🔄 Обновления:

Для обновления бота:
```bash
sudo ./bot_manager.sh stop
sudo ./bot_manager.sh backup
# Загрузите новые файлы
sudo ./bot_manager.sh update
```

## 🆘 Устранение неполадок:

1. **Проверьте логи**: `sudo ./bot_manager.sh logs`
2. **Проверьте nginx**: `sudo nginx -t`
3. **Проверьте SSL**: `sudo certbot certificates`
4. **Проверьте права**: `sudo chown -R www-data:www-data /opt/telegram_bot`

Ваш бот готов к работе в продакшене! 🎉
