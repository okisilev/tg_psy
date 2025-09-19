#!/bin/bash

# 🔒 СКРИПТ РАЗВЕРТЫВАНИЯ С SSL И NGINX
# Использование: ./deploy_ssl.sh yourdomain.com

if [ $# -eq 0 ]; then
    echo "❌ Ошибка: Укажите домен"
    echo "Использование: ./deploy_ssl.sh yourdomain.com"
    echo "Пример: ./deploy_ssl.sh mydomain.com"
    exit 1
fi

DOMAIN=$1
PROJECT_DIR="/opt/tg_psy"

echo "🔒 РАЗВЕРТЫВАНИЕ С SSL И NGINX"
echo "=" * 60
echo "Домен: $DOMAIN"
echo "Директория проекта: $PROJECT_DIR"
echo ""

# 1. Обновление системы
echo "📦 Обновление системы..."
sudo apt update && sudo apt upgrade -y

# 2. Установка зависимостей
echo "🔧 Установка зависимостей..."
sudo apt install python3 python3-pip python3-venv curl wget git nginx certbot python3-certbot-nginx -y

# 3. Создание директории проекта
echo "📁 Создание директории проекта..."
sudo mkdir -p $PROJECT_DIR
sudo chown $USER:$USER $PROJECT_DIR

# 4. Копирование файлов проекта
echo "📋 Копирование файлов проекта..."
cp -r . $PROJECT_DIR/
cd $PROJECT_DIR

# 5. Создание виртуального окружения
echo "🐍 Создание виртуального окружения..."
python3 -m venv venv
source venv/bin/activate

# 6. Установка Python пакетов
echo "📦 Установка Python пакетов..."
pip install flask requests python-telegram-bot

# 7. Создание .env файла
echo "⚙️ Создание .env файла..."
cat > .env << EOF
# Telegram Bot Configuration
BOT_TOKEN=8455794146:AAFf9DEcTxLnJfG-HWWmzwpSjTRDzNE3px8
ADMIN_CHAT_ID=431292182,190545165
ADMIN_IDS=431292182,190545165
CHANNEL_ID=-1001234567890
CHANNEL_USERNAME=@your_channel_username
CHANNEL_INVITE_LINK=https://t.me/+gstVWYW2Kgo2OGYy

# Prodamus Configuration
PRODAMUS_SHOP_ID=dashastar
PRODAMUS_SECRET_KEY=b2f9e8a399225271521dfe88a277a7371cb8c2cebfeaa6f0276ba81fcc303c93
PRODAMUS_DEMO_MODE=true
PRODAMUS_WEBHOOK_URL=https://$DOMAIN/sales/prodamus

# Webhook Configuration
WEBHOOK_URL=https://$DOMAIN/webhook/telegram
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
DEBUG=false
EOF

# 8. Инициализация базы данных
echo "🗄️ Инициализация базы данных..."
python3 -c "from database import Database; db = Database(); print('База данных инициализирована')"

# 9. Настройка файрвола
echo "🔥 Настройка файрвола..."
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw allow 5000
sudo ufw --force enable

# 10. Настройка Nginx с SSL
echo "🌐 Настройка Nginx с SSL..."
sudo tee /etc/nginx/sites-available/tg_psy << EOF
# HTTP редирект на HTTPS
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;
    return 301 https://\$server_name\$request_uri;
}

# HTTPS конфигурация
server {
    listen 443 ssl http2;
    server_name $DOMAIN www.$DOMAIN;
    
    # SSL сертификаты (будут установлены позже)
    # ssl_certificate /etc/letsencrypt/live/$DOMAIN/fullchain.pem;
    # ssl_certificate_key /etc/letsencrypt/live/$DOMAIN/privkey.pem;
    
    # SSL настройки
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # Безопасность
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    
    # Логирование
    access_log /var/log/nginx/tg_psy_access.log;
    error_log /var/log/nginx/tg_psy_error.log;
    
    # Webhook для Telegram бота
    location /webhook/telegram {
        proxy_pass http://localhost:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_set_header X-Forwarded-Host \$host;
        proxy_set_header X-Forwarded-Port \$server_port;
        
        # Таймауты
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
        
        # Буферизация
        proxy_buffering on;
        proxy_buffer_size 4k;
        proxy_buffers 8 4k;
        
        # Размеры запросов
        client_max_body_size 1M;
    }
    
    # Webhook для Prodamus
    location /sales/prodamus {
        proxy_pass http://localhost:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_set_header X-Forwarded-Host \$host;
        proxy_set_header X-Forwarded-Port \$server_port;
        
        # Таймауты
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
        
        # Буферизация
        proxy_buffering on;
        proxy_buffer_size 4k;
        proxy_buffers 8 4k;
        
        # Размеры запросов
        client_max_body_size 1M;
        
        # Дополнительные заголовки для Prodamus
        proxy_set_header X-Forwarded-Ssl on;
    }
    
    # Health check endpoint
    location /health {
        proxy_pass http://localhost:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
    
    # Статус endpoint
    location /status {
        proxy_pass http://localhost:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
    
    # Блокировка доступа к системным файлам
    location ~ /\. {
        deny all;
        access_log off;
        log_not_found off;
    }
    
    # Блокировка доступа к конфигурационным файлам
    location ~ \.(env|ini|conf)$ {
        deny all;
        access_log off;
        log_not_found off;
    }
    
    # Gzip сжатие
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/json
        application/javascript
        application/xml+rss
        application/atom+xml
        image/svg+xml;
}
EOF

# 11. Активация конфигурации Nginx
echo "🔗 Активация конфигурации Nginx..."
sudo ln -s /etc/nginx/sites-available/tg_psy /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# 12. Проверка конфигурации Nginx
echo "🔍 Проверка конфигурации Nginx..."
sudo nginx -t

if [ $? -ne 0 ]; then
    echo "❌ Ошибка в конфигурации Nginx"
    exit 1
fi

# 13. Перезапуск Nginx
echo "🔄 Перезапуск Nginx..."
sudo systemctl restart nginx
sudo systemctl enable nginx

# 14. Получение SSL сертификата
echo "🔒 Получение SSL сертификата..."
sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN

# 15. Настройка systemd сервисов
echo "🔧 Настройка systemd сервисов..."

# Webhook сервис
sudo tee /etc/systemd/system/tg-psy-webhook.service << EOF
[Unit]
Description=TG Psy Webhook Server
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=$PROJECT_DIR
Environment=PATH=$PROJECT_DIR/venv/bin
ExecStart=$PROJECT_DIR/venv/bin/python webhook_ssl.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Telegram Bot сервис
sudo tee /etc/systemd/system/tg-psy-bot.service << EOF
[Unit]
Description=TG Psy Telegram Bot
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=$PROJECT_DIR
Environment=PATH=$PROJECT_DIR/venv/bin
ExecStart=$PROJECT_DIR/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 16. Активация сервисов
echo "🚀 Активация сервисов..."
sudo systemctl daemon-reload
sudo systemctl enable tg-psy-webhook
sudo systemctl enable tg-psy-bot
sudo systemctl start tg-psy-webhook
sudo systemctl start tg-psy-bot

# 17. Настройка автоматического обновления SSL
echo "🔄 Настройка автоматического обновления SSL..."
sudo crontab -l 2>/dev/null | grep -v "certbot" | sudo crontab -
echo "0 12 * * * /usr/bin/certbot renew --quiet" | sudo crontab -

# 18. Проверка SSL
echo "🔍 Проверка SSL сертификата..."
sudo certbot certificates

# 19. Проверка статуса
echo "🔍 Проверка статуса сервисов..."
sudo systemctl status tg-psy-webhook --no-pager
sudo systemctl status tg-psy-bot --no-pager

# 20. Тестирование endpoints
echo "🧪 Тестирование endpoints..."
echo "   - Health check: https://$DOMAIN/health"
echo "   - Telegram webhook: https://$DOMAIN/webhook/telegram"
echo "   - Prodamus webhook: https://$DOMAIN/sales/prodamus"

# Проверка доступности
curl -I https://$DOMAIN/health

echo ""
echo "🎉 РАЗВЕРТЫВАНИЕ С SSL ЗАВЕРШЕНО!"
echo ""
echo "📝 Следующие шаги:"
echo "   1. Настройте webhook URL в панели Prodamus: https://$DOMAIN/sales/prodamus"
echo "   2. Настройте webhook URL в Telegram Bot API: https://$DOMAIN/webhook/telegram"
echo "   3. Протестируйте создание платежа"
echo "   4. Проверьте получение webhook уведомлений"
echo ""
echo "🔍 Мониторинг:"
echo "   - Логи webhook: sudo journalctl -u tg-psy-webhook -f"
echo "   - Логи бота: sudo journalctl -u tg-psy-bot -f"
echo "   - Логи Nginx: sudo tail -f /var/log/nginx/tg_psy_access.log"
echo "   - Статус SSL: sudo certbot certificates"
echo ""
echo "✅ Система готова к работе с SSL!"
