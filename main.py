#!/usr/bin/env python3
"""
Главный файл для запуска Telegram бота Женского клуба
"""

import asyncio
import logging
import signal
import sys
from threading import Thread
from bot import WomenClubBot
from webhook import app

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class ApplicationManager:
    def __init__(self):
        self.bot = WomenClubBot()
        self.webhook_thread = None
        self.is_running = False
    
    def start_webhook_server(self):
        """Запуск webhook сервера в отдельном потоке"""
        logger.info("Запуск webhook сервера...")
        app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
    
    def signal_handler(self, signum, frame):
        """Обработчик сигналов для корректного завершения"""
        logger.info(f"Получен сигнал {signum}, завершение работы...")
        self.stop()
        sys.exit(0)
    
    def start(self):
        """Запуск приложения"""
        try:
            self.is_running = True
            
            # Регистрируем обработчики сигналов
            signal.signal(signal.SIGINT, self.signal_handler)
            signal.signal(signal.SIGTERM, self.signal_handler)
            
            # Запускаем webhook сервер в отдельном потоке
            self.webhook_thread = Thread(target=self.start_webhook_server, daemon=True)
            self.webhook_thread.start()
            
            logger.info("Приложение запущено")
            logger.info("Webhook сервер: http://localhost:5000")
            logger.info("Для остановки нажмите Ctrl+C")
            
            # Запускаем бота (блокирующий вызов)
            self.bot.run()
            
        except KeyboardInterrupt:
            logger.info("Получен сигнал прерывания")
        except Exception as e:
            logger.error(f"Ошибка запуска приложения: {e}")
        finally:
            self.stop()
    
    def stop(self):
        """Остановка приложения"""
        if self.is_running:
            logger.info("Остановка приложения...")
            self.is_running = False
            
            # Останавливаем планировщик
            try:
                asyncio.run(self.bot.scheduler.stop())
            except Exception as e:
                logger.error(f"Ошибка остановки планировщика: {e}")
            
            # Закрываем базу данных
            try:
                self.bot.db.close()
            except Exception as e:
                logger.error(f"Ошибка закрытия базы данных: {e}")
            
            logger.info("Приложение остановлено")

def main():
    """Главная функция"""
    print("=" * 50)
    print("🤖 Telegram Bot для Женского клуба")
    print("=" * 50)
    
    app_manager = ApplicationManager()
    app_manager.start()

if __name__ == "__main__":
    main()
