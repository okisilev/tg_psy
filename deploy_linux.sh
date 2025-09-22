#!/bin/bash

# 🚀 СКРИПТ АВТОМАТИЧЕСКОГО РАЗВЕРТЫВАНИЯ НА LINUX
# Использование: ./deploy_linux.sh YOUR_DOMAIN.com

if [ $# -eq 0 ]; then
    echo "❌ Ошибка: Укажите домен"
    echo "Использование: ./deploy_linux.sh YOUR_DOMAIN.com"
    echo "Пример: ./deploy_linux.sh mydomain.com"
    exit 1
fi

DOMAIN=$1
PROJECT_DIR="/opt/tg_psy"

echo "🚀 АВТОМАТИЧЕСКОЕ РАЗВЕРТЫВАНИЕ НА LINUX"
echo "=" * 60
echo "Домен: $DOMAIN"
echo "Директория проекта: $PROJECT_DIR"
echo ""

# 1. Обновление системы
echo "📦 Обновление системы..."
sudo apt update && sudo apt upgrade -y

# 2. Установка зависимостей
echo "🔧 Установка зависимостей..."
sudo apt install python3 python3-pip python3-venv curl wget git nginx certbot -y

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

# 9. Настройка Nginx
echo "🌐 Настройка Nginx..."
sudo tee /etc/nginx/sites-available/tg_psy << EOF
server {
    listen 80;
    server_name $DOMAIN;
    
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

# Активация конфигурации Nginx
sudo ln -s /etc/nginx/sites-available/tg_psy /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# 10. Настройка systemd сервисов
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
ExecStart=$PROJECT_DIR/venv/bin/python webhook_http.py
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

# 11. Настройка файрвола
echo "🔥 Настройка файрвола..."
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw allow 5000
sudo ufw --force enable

# 12. Активация сервисов
echo "🚀 Активация сервисов..."
sudo systemctl daemon-reload
sudo systemctl enable tg-psy-webhook
sudo systemctl enable tg-psy-bot
sudo systemctl start tg-psy-webhook
sudo systemctl start tg-psy-bot

# 13. Получение SSL сертификата
echo "🔒 Получение SSL сертификата..."
sudo certbot --nginx -d $DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN

# 14. Проверка статуса
echo "🔍 Проверка статуса сервисов..."
sudo systemctl status tg-psy-webhook --no-pager
sudo systemctl status tg-psy-bot --no-pager

echo ""
echo "🎉 РАЗВЕРТЫВАНИЕ ЗАВЕРШЕНО!"
echo ""
echo "📝 Следующие шаги:"
echo "   1. Настройте webhook URL в панели Prodamus: https://$DOMAIN/sales/prodamus"
echo "   2. Протестируйте создание платежа"
echo "   3. Проверьте получение webhook уведомлений"
echo ""
echo "🔍 Проверка системы:"
echo "   - Health check: https://$DOMAIN/health"
echo "   - Webhook: https://$DOMAIN/sales/prodamus"
echo "   - Логи webhook: sudo journalctl -u tg-psy-webhook -f"
echo "   - Логи бота: sudo journalctl -u tg-psy-bot -f"
echo ""
echo "✅ Система готова к работе!"
