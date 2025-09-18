#!/bin/bash

# Скрипт для деплоя Telegram бота на продакшен сервер
# Использование: ./deploy.sh

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Конфигурация
BOT_DIR="/usr/TG_BOTs/tg_psy"
SERVICE_NAME="tg_psy"
NGINX_SITE="tg_psy"

echo -e "${GREEN}🚀 Начинаем деплой Telegram бота...${NC}"

# Проверяем права sudo
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}❌ Запустите скрипт с правами sudo${NC}"
    exit 1
fi

# Создаем директорию для бота
echo -e "${YELLOW}📁 Создаем директорию для бота...${NC}"
mkdir -p $BOT_DIR
cd $BOT_DIR

# Создаем виртуальное окружение
echo -e "${YELLOW}🐍 Создаем виртуальное окружение...${NC}"
python3 -m venv venv
source venv/bin/activate

# Устанавливаем зависимости
echo -e "${YELLOW}📦 Устанавливаем зависимости...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

# Копируем файлы бота
echo -e "${YELLOW}📋 Копируем файлы бота...${NC}"
cp bot_webhook.py $BOT_DIR/
cp admin_panel.py $BOT_DIR/
cp channel_manager.py $BOT_DIR/
cp config.py $BOT_DIR/
cp database.py $BOT_DIR/
cp prodamus.py $BOT_DIR/
cp scheduler.py $BOT_DIR/
cp init_db.py $BOT_DIR/

# Создаем директории для логов
mkdir -p logs
mkdir -p ssl

# Устанавливаем права доступа
chown -R www-data:www-data $BOT_DIR
chmod -R 755 $BOT_DIR

# Копируем systemd сервис
echo -e "${YELLOW}⚙️ Настраиваем systemd сервис...${NC}"
cp telegram_bot.service /etc/systemd/system/
sed -i "s|/path/to/your/bot/directory|$BOT_DIR|g" /etc/systemd/system/telegram_bot.service

# Перезагружаем systemd и включаем сервис
systemctl daemon-reload
systemctl enable $SERVICE_NAME

# Копируем конфигурацию nginx
echo -e "${YELLOW}🌐 Настраиваем nginx...${NC}"
cp nginx_config.conf /etc/nginx/sites-available/$NGINX_SITE

# Создаем символическую ссылку
ln -sf /etc/nginx/sites-available/$NGINX_SITE /etc/nginx/sites-enabled/

# Проверяем конфигурацию nginx
nginx -t

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Конфигурация nginx корректна${NC}"
else
    echo -e "${RED}❌ Ошибка в конфигурации nginx${NC}"
    exit 1
fi

# Перезапускаем nginx
systemctl reload nginx

# Инициализируем базу данных
echo -e "${YELLOW}🗄️ Инициализируем базу данных...${NC}"
cd $BOT_DIR
source venv/bin/activate
python init_db.py

# Запускаем бота
echo -e "${YELLOW}🤖 Запускаем бота...${NC}"
systemctl start $SERVICE_NAME

# Проверяем статус
sleep 5
if systemctl is-active --quiet $SERVICE_NAME; then
    echo -e "${GREEN}✅ Бот успешно запущен!${NC}"
    echo -e "${GREEN}📊 Статус сервиса:${NC}"
    systemctl status $SERVICE_NAME --no-pager
else
    echo -e "${RED}❌ Ошибка запуска бота${NC}"
    echo -e "${RED}📋 Логи сервиса:${NC}"
    journalctl -u $SERVICE_NAME --no-pager -n 20
    exit 1
fi

echo -e "${GREEN}🎉 Деплой завершен успешно!${NC}"
echo -e "${YELLOW}📝 Следующие шаги:${NC}"
echo -e "1. Отредактируйте файл .env с вашими настройками"
echo -e "2. Обновите конфигурацию nginx с вашим доменом"
echo -e "3. Убедитесь, что SSL сертификаты настроены"
echo -e "4. Проверьте webhook: https://yourdomain.com/health"
echo -e ""
echo -e "${YELLOW}🔧 Полезные команды:${NC}"
echo -e "systemctl status $SERVICE_NAME    # Статус бота"
echo -e "systemctl restart $SERVICE_NAME   # Перезапуск бота"
echo -e "journalctl -u $SERVICE_NAME -f    # Просмотр логов в реальном времени"
echo -e "systemctl stop $SERVICE_NAME      # Остановка бота"
