# 🚀 ОТЧЕТ О ГОТОВНОСТИ К РАЗВЕРТЫВАНИЮ

## ✅ Статус готовности: 6/7 проверок пройдено

### 🎯 Что готово:

1. **✅ Системные требования**: Python 3.13.2, порты свободны
2. **✅ Конфигурация**: Все переменные окружения установлены
3. **✅ Файлы проекта**: Все необходимые файлы на месте
4. **✅ База данных**: Инициализирована, все таблицы созданы
5. **✅ Webhook конфигурация**: URL настроен корректно
6. **✅ Linux настройки**: Права доступа в порядке

### ⚠️ Что требует внимания:

1. **❌ Python пакеты**: Не установлен `python-telegram-bot`
   - **Решение**: `pip install python-telegram-bot`

## 🔧 Текущая конфигурация

### Порт webhook: 5000 ✅
- **Flask Host**: `0.0.0.0`
- **Flask Port**: `5000`
- **Webhook URL**: `http://82.147.71.224:5000/sales/prodamus`

### Переменные окружения:
- ✅ `BOT_TOKEN`: Установлен
- ✅ `ADMIN_CHAT_ID`: Установлен
- ✅ `CHANNEL_ID`: Установлен
- ✅ `PRODAMUS_SHOP_ID`: `dashastar`
- ✅ `PRODAMUS_SECRET_KEY`: Установлен
- ✅ `PRODAMUS_WEBHOOK_URL`: `http://82.147.71.224:5000/sales/prodamus`

## 📋 Чек-лист для Linux сервера

### 1. Установка зависимостей
```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Python и pip
sudo apt install python3 python3-pip python3-venv -y

# Установка дополнительных пакетов
sudo apt install curl wget git nginx certbot -y

# Создание виртуального окружения
python3 -m venv venv
source venv/bin/activate

# Установка Python пакетов
pip install flask requests python-telegram-bot
```

### 2. Настройка проекта
```bash
# Клонирование проекта
git clone <repository_url> /opt/tg_psy
cd /opt/tg_psy

# Создание .env файла
cat > .env << 'EOF'
BOT_TOKEN=8455794146:AAFf9DEcTxLnJfG-HWWmzwpSjTRDzNE3px8
ADMIN_CHAT_ID=431292182,190545165
ADMIN_IDS=431292182,190545165
CHANNEL_ID=-1001234567890
CHANNEL_USERNAME=@your_channel_username
CHANNEL_INVITE_LINK=https://t.me/+gstVWYW2Kgo2OGYy
PRODAMUS_SHOP_ID=dashastar
PRODAMUS_SECRET_KEY=b2f9e8a399225271521dfe88a277a7371cb8c2cebfeaa6f0276ba81fcc303c93
PRODAMUS_DEMO_MODE=true
PRODAMUS_WEBHOOK_URL=http://YOUR_DOMAIN.com:5000/sales/prodamus
WEBHOOK_URL=http://YOUR_DOMAIN.com:5000/webhook/telegram
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
DEBUG=false
EOF
```

### 3. Настройка Nginx
```bash
# Создание конфигурации Nginx
sudo tee /etc/nginx/sites-available/tg_psy << 'EOF'
server {
    listen 80;
    server_name YOUR_DOMAIN.com;
    
    location /webhook/telegram {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /sales/prodamus {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /health {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
EOF

# Активация конфигурации
sudo ln -s /etc/nginx/sites-available/tg_psy /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 4. Настройка SSL
```bash
# Получение SSL сертификата
sudo certbot --nginx -d YOUR_DOMAIN.com
```

### 5. Настройка systemd сервисов
```bash
# Webhook сервис
sudo tee /etc/systemd/system/tg-psy-webhook.service << 'EOF'
[Unit]
Description=TG Psy Webhook Server
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/tg_psy
Environment=PATH=/opt/tg_psy/venv/bin
ExecStart=/opt/tg_psy/venv/bin/python webhook_http.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Telegram Bot сервис
sudo tee /etc/systemd/system/tg-psy-bot.service << 'EOF'
[Unit]
Description=TG Psy Telegram Bot
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/tg_psy
Environment=PATH=/opt/tg_psy/venv/bin
ExecStart=/opt/tg_psy/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Активация сервисов
sudo systemctl daemon-reload
sudo systemctl enable tg-psy-webhook
sudo systemctl enable tg-psy-bot
sudo systemctl start tg-psy-webhook
sudo systemctl start tg-psy-bot
```

## 🧪 Тестирование на сервере

### 1. Проверка сервисов
```bash
# Статус сервисов
sudo systemctl status tg-psy-webhook
sudo systemctl status tg-psy-bot

# Логи
sudo journalctl -u tg-psy-webhook -f
sudo journalctl -u tg-psy-bot -f
```

### 2. Проверка webhook
```bash
# Health check
curl http://YOUR_DOMAIN.com/health

# Тест webhook
curl -X POST http://YOUR_DOMAIN.com/sales/prodamus \
  -H "Content-Type: application/json" \
  -H "Sign: test_signature" \
  -d '{"test": "data"}'
```

### 3. Проверка конфигурации
```bash
cd /opt/tg_psy
source venv/bin/activate
python3 check_linux_deployment.py
```

## 📝 Настройка в панели Prodamus

### Webhook URL:
- **URL**: `https://YOUR_DOMAIN.com/sales/prodamus`
- **Метод**: POST
- **Заголовки**: `Sign: {signature}`

### Настройки магазина:
- **Shop ID**: `dashastar`
- **Secret Key**: `b2f9e8a399225271521dfe88a277a7371cb8c2cebfeaa6f0276ba81fcc303c93`
- **Demo Mode**: Включен для тестирования

## 🔍 Мониторинг

### Логи:
```bash
# Логи webhook
sudo journalctl -u tg-psy-webhook -f

# Логи бота
sudo journalctl -u tg-psy-bot -f

# Логи Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Мониторинг ресурсов:
```bash
# Использование ресурсов
htop
df -h
free -h

# Проверка портов
netstat -tlnp | grep :5000
```

## ⚠️ Важные замечания

### Безопасность:
- ✅ Используйте HTTPS для продакшена
- ✅ Настройте файрвол
- ✅ Регулярно обновляйте систему
- ✅ Используйте сильные пароли

### Резервное копирование:
- ✅ Регулярно создавайте резервные копии базы данных
- ✅ Сохраняйте конфигурационные файлы
- ✅ Документируйте изменения

---

**Система готова к развертыванию на Linux сервере! 🚀**

**Осталось только:**
1. Установить `python-telegram-bot`: `pip install python-telegram-bot`
2. Загрузить файлы на сервер
3. Настроить домен и SSL
4. Запустить сервисы
