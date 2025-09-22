#!/usr/bin/env python3
"""
Главный файл для запуска Telegram бота Женского клуба с webhook сервером
"""

import asyncio
import logging
import signal
import sys
import time
from threading import Thread
from bot import WomenClubBot
from webhook import app
from config import FLASK_HOST, FLASK_PORT

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
        logger.info("🚀 Запуск webhook сервера...")
        logger.info(f"   - Host: {FLASK_HOST}")
        logger.info(f"   - Port: {FLASK_PORT}")
        logger.info(f"   - URL: http://{FLASK_HOST}:{FLASK_PORT}")
        
        try:
            app.run(host=FLASK_HOST, port=FLASK_PORT, debug=False, use_reloader=False)
        except Exception as e:
            logger.error(f"Ошибка запуска webhook сервера: {e}")
    
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
            logger.info("🌐 Запуск webhook сервера в отдельном потоке...")
            self.webhook_thread = Thread(target=self.start_webhook_server, daemon=True)
            self.webhook_thread.start()
            
            # Ждем запуска webhook сервера
            logger.info("⏳ Ожидание запуска webhook сервера...")
            time.sleep(5)
            
            # Проверяем webhook сервер
            try:
                import requests
                response = requests.get(f"http://{FLASK_HOST}:{FLASK_PORT}/health", timeout=5)
                if response.status_code == 200:
                    logger.info("✅ Webhook сервер запущен успешно")
                else:
                    logger.warning(f"⚠️ Webhook сервер отвечает с кодом {response.status_code}")
            except Exception as e:
                logger.warning(f"⚠️ Не удалось проверить webhook сервер: {e}")
            
            logger.info("🤖 Запуск Telegram бота...")
            logger.info("   - Webhook сервер: http://localhost:5000")
            logger.info("   - Для остановки нажмите Ctrl+C")
            
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
            logger.info("🛑 Остановка приложения...")
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
            
            logger.info("✅ Приложение остановлено")

def main():
    """Главная функция"""
    print("=" * 50)
    print("🤖 Telegram Bot для Женского клуба")
    print("🌐 С webhook сервером")
    print("=" * 50)
    
    app_manager = ApplicationManager()
    app_manager.start()

if __name__ == "__main__":
    main()
