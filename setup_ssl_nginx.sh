#!/bin/bash

# 🔒 СКРИПТ НАСТРОЙКИ SSL И NGINX ДЛЯ WEBHOOK
# Использование: ./setup_ssl_nginx.sh yourdomain.com

if [ $# -eq 0 ]; then
    echo "❌ Ошибка: Укажите домен"
    echo "Использование: ./setup_ssl_nginx.sh yourdomain.com"
    echo "Пример: ./setup_ssl_nginx.sh mydomain.com"
    exit 1
fi

DOMAIN=$1

echo "🔒 НАСТРОЙКА SSL И NGINX ДЛЯ WEBHOOK"
echo "=" * 60
echo "Домен: $DOMAIN"
echo ""

# 1. Обновление системы
echo "📦 Обновление системы..."
sudo apt update && sudo apt upgrade -y

# 2. Установка Nginx и Certbot
echo "🌐 Установка Nginx и Certbot..."
sudo apt install nginx certbot python3-certbot-nginx -y

# 3. Настройка файрвола
echo "🔥 Настройка файрвола..."
sudo ufw allow 'Nginx Full'
sudo ufw allow ssh
sudo ufw --force enable

# 4. Создание базовой конфигурации Nginx
echo "⚙️ Создание базовой конфигурации Nginx..."
sudo tee /etc/nginx/sites-available/tg_psy << EOF
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;
    
    location /webhook/telegram {
        proxy_pass http://localhost:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
    
    location /sales/prodamus {
        proxy_pass http://localhost:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
    
    location /health {
        proxy_pass http://localhost:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF

# 5. Активация конфигурации
echo "🔗 Активация конфигурации Nginx..."
sudo ln -s /etc/nginx/sites-available/tg_psy /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# 6. Проверка конфигурации
echo "🔍 Проверка конфигурации Nginx..."
sudo nginx -t

if [ $? -ne 0 ]; then
    echo "❌ Ошибка в конфигурации Nginx"
    exit 1
fi

# 7. Перезапуск Nginx
echo "🔄 Перезапуск Nginx..."
sudo systemctl restart nginx
sudo systemctl enable nginx

# 8. Получение SSL сертификата
echo "🔒 Получение SSL сертификата..."
sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN

# 9. Создание полной SSL конфигурации
echo "⚙️ Создание полной SSL конфигурации..."
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
    
    # SSL сертификаты
    ssl_certificate /etc/letsencrypt/live/$DOMAIN/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/$DOMAIN/privkey.pem;
    
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

# 10. Проверка и перезапуск Nginx
echo "🔍 Проверка конфигурации Nginx..."
sudo nginx -t

if [ $? -ne 0 ]; then
    echo "❌ Ошибка в конфигурации Nginx"
    exit 1
fi

echo "🔄 Перезапуск Nginx..."
sudo systemctl reload nginx

# 11. Настройка автоматического обновления SSL
echo "🔄 Настройка автоматического обновления SSL..."
sudo crontab -l 2>/dev/null | grep -v "certbot" | sudo crontab -
echo "0 12 * * * /usr/bin/certbot renew --quiet" | sudo crontab -

# 12. Проверка SSL
echo "🔍 Проверка SSL сертификата..."
sudo certbot certificates

# 13. Тестирование endpoints
echo "🧪 Тестирование endpoints..."
echo "   - Health check: https://$DOMAIN/health"
echo "   - Telegram webhook: https://$DOMAIN/webhook/telegram"
echo "   - Prodamus webhook: https://$DOMAIN/sales/prodamus"

# Проверка доступности
curl -I https://$DOMAIN/health

echo ""
echo "🎉 SSL И NGINX НАСТРОЕНЫ!"
echo ""
echo "📝 Следующие шаги:"
echo "   1. Настройте webhook URL в панели Prodamus: https://$DOMAIN/sales/prodamus"
echo "   2. Настройте webhook URL в Telegram Bot API: https://$DOMAIN/webhook/telegram"
echo "   3. Протестируйте создание платежа"
echo "   4. Проверьте получение webhook уведомлений"
echo ""
echo "🔍 Мониторинг:"
echo "   - Логи Nginx: sudo tail -f /var/log/nginx/tg_psy_access.log"
echo "   - Логи ошибок: sudo tail -f /var/log/nginx/tg_psy_error.log"
echo "   - Статус SSL: sudo certbot certificates"
echo ""
echo "✅ Система готова к работе с SSL!"
