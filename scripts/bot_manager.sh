#!/bin/bash

# Скрипт для управления Telegram ботом
# Использование: ./bot_manager.sh [start|stop|restart|status|logs|update]

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

SERVICE_NAME="telegram_bot"
BOT_DIR="/opt/telegram_bot"

show_usage() {
    echo -e "${BLUE}Использование: $0 [команда]${NC}"
    echo -e "${YELLOW}Доступные команды:${NC}"
    echo -e "  start    - Запустить бота"
    echo -e "  stop     - Остановить бота"
    echo -e "  restart  - Перезапустить бота"
    echo -e "  status   - Показать статус бота"
    echo -e "  logs     - Показать логи бота"
    echo -e "  update   - Обновить код бота"
    echo -e "  health   - Проверить здоровье бота"
    echo -e "  backup   - Создать бэкап базы данных"
}

start_bot() {
    echo -e "${YELLOW}🚀 Запускаем бота...${NC}"
    systemctl start $SERVICE_NAME
    sleep 3
    if systemctl is-active --quiet $SERVICE_NAME; then
        echo -e "${GREEN}✅ Бот успешно запущен!${NC}"
    else
        echo -e "${RED}❌ Ошибка запуска бота${NC}"
        exit 1
    fi
}

stop_bot() {
    echo -e "${YELLOW}🛑 Останавливаем бота...${NC}"
    systemctl stop $SERVICE_NAME
    echo -e "${GREEN}✅ Бот остановлен${NC}"
}

restart_bot() {
    echo -e "${YELLOW}🔄 Перезапускаем бота...${NC}"
    systemctl restart $SERVICE_NAME
    sleep 3
    if systemctl is-active --quiet $SERVICE_NAME; then
        echo -e "${GREEN}✅ Бот успешно перезапущен!${NC}"
    else
        echo -e "${RED}❌ Ошибка перезапуска бота${NC}"
        exit 1
    fi
}

show_status() {
    echo -e "${BLUE}📊 Статус бота:${NC}"
    systemctl status $SERVICE_NAME --no-pager
    
    echo -e "\n${BLUE}📈 Статистика:${NC}"
    curl -s http://localhost:5000/status | jq '.' 2>/dev/null || echo "Не удалось получить статистику"
}

show_logs() {
    echo -e "${BLUE}📋 Логи бота (последние 50 строк):${NC}"
    journalctl -u $SERVICE_NAME --no-pager -n 50
}

update_bot() {
    echo -e "${YELLOW}📦 Обновляем код бота...${NC}"
    
    # Останавливаем бота
    systemctl stop $SERVICE_NAME
    
    # Создаем бэкап
    backup_db
    
    # Копируем новые файлы
    cp bot_webhook.py $BOT_DIR/
    cp admin_panel.py $BOT_DIR/
    cp channel_manager.py $BOT_DIR/
    cp config.py $BOT_DIR/
    cp database.py $BOT_DIR/
    cp prodamus.py $BOT_DIR/
    cp scheduler.py $BOT_DIR/
    
    # Устанавливаем права
    chown -R www-data:www-data $BOT_DIR
    
    # Перезагружаем systemd
    systemctl daemon-reload
    
    # Запускаем бота
    systemctl start $SERVICE_NAME
    
    sleep 3
    if systemctl is-active --quiet $SERVICE_NAME; then
        echo -e "${GREEN}✅ Бот успешно обновлен и запущен!${NC}"
    else
        echo -e "${RED}❌ Ошибка после обновления${NC}"
        exit 1
    fi
}

check_health() {
    echo -e "${BLUE}🏥 Проверяем здоровье бота...${NC}"
    
    # Проверяем статус сервиса
    if systemctl is-active --quiet $SERVICE_NAME; then
        echo -e "${GREEN}✅ Сервис запущен${NC}"
    else
        echo -e "${RED}❌ Сервис не запущен${NC}"
        return 1
    fi
    
    # Проверяем HTTP endpoint
    if curl -s http://localhost:5000/health > /dev/null; then
        echo -e "${GREEN}✅ HTTP endpoint отвечает${NC}"
    else
        echo -e "${RED}❌ HTTP endpoint не отвечает${NC}"
        return 1
    fi
    
    # Проверяем базу данных
    if [ -f "$BOT_DIR/women_club.db" ]; then
        echo -e "${GREEN}✅ База данных существует${NC}"
    else
        echo -e "${RED}❌ База данных не найдена${NC}"
        return 1
    fi
    
    echo -e "${GREEN}🎉 Все проверки пройдены успешно!${NC}"
}

backup_db() {
    echo -e "${YELLOW}💾 Создаем бэкап базы данных...${NC}"
    
    BACKUP_DIR="$BOT_DIR/backups"
    mkdir -p $BACKUP_DIR
    
    TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
    BACKUP_FILE="$BACKUP_DIR/women_club_$TIMESTAMP.db"
    
    cp "$BOT_DIR/women_club.db" "$BACKUP_FILE"
    
    # Удаляем старые бэкапы (оставляем последние 10)
    cd $BACKUP_DIR
    ls -t women_club_*.db | tail -n +11 | xargs -r rm
    
    echo -e "${GREEN}✅ Бэкап создан: $BACKUP_FILE${NC}"
}

# Проверяем права sudo
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}❌ Запустите скрипт с правами sudo${NC}"
    exit 1
fi

# Обработка команд
case "$1" in
    start)
        start_bot
        ;;
    stop)
        stop_bot
        ;;
    restart)
        restart_bot
        ;;
    status)
        show_status
        ;;
    logs)
        show_logs
        ;;
    update)
        update_bot
        ;;
    health)
        check_health
        ;;
    backup)
        backup_db
        ;;
    *)
        show_usage
        exit 1
        ;;
esac
