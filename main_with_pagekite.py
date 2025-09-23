#!/usr/bin/env python3
"""
Главный файл для запуска Telegram бота с webhook сервером и PageKite
"""

import asyncio
import logging
import signal
import sys
import time
import subprocess
import os
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
        self.pagekite_process = None
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
    
    def start_pagekite(self):
        """Запуск PageKite"""
        logger.info("🌐 Запуск PageKite...")
        logger.info("   - Domain: dashastar.pagekite.me")
        logger.info("   - Port: 5000")
        
        try:
            # Проверяем наличие pagekite.py
            if not os.path.exists('pagekite.py'):
                logger.error("❌ Файл pagekite.py не найден!")
                logger.info("📥 Скачивание pagekite.py...")
                try:
                    import urllib.request
                    urllib.request.urlretrieve('https://pagekite.net/pk/pagekite.py', 'pagekite.py')
                    os.chmod('pagekite.py', 0o755)
                    logger.info("✅ pagekite.py скачан и настроен")
                except Exception as e:
                    logger.error(f"Ошибка скачивания pagekite.py: {e}")
                    return
            
            # Запускаем PageKite
            self.pagekite_process = subprocess.Popen(
                ['./pagekite.py', '5000', 'dashastar.pagekite.me'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            logger.info(f"✅ PageKite запущен (PID: {self.pagekite_process.pid})")
            
            # Ждем немного для инициализации
            time.sleep(10)
            
            # Проверяем статус PageKite
            try:
                import requests
                response = requests.get("https://dashastar.pagekite.me/health", timeout=10)
                if response.status_code == 200:
                    logger.info("✅ PageKite работает и доступен")
                else:
                    logger.warning(f"⚠️ PageKite отвечает с кодом {response.status_code}")
            except Exception as e:
                logger.warning(f"⚠️ Не удалось проверить PageKite: {e}")
                
        except Exception as e:
            logger.error(f"Ошибка запуска PageKite: {e}")
    
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
            
            # Запускаем PageKite
            self.start_pagekite()
            
            logger.info("🤖 Запуск Telegram бота...")
            logger.info("   - Webhook сервер: http://localhost:5000")
            logger.info("   - PageKite: https://dashastar.pagekite.me")
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
            
            # Останавливаем PageKite
            if self.pagekite_process:
                logger.info("⏹️ Остановка PageKite...")
                try:
                    self.pagekite_process.terminate()
                    self.pagekite_process.wait(timeout=5)
                    logger.info("✅ PageKite остановлен")
                except Exception as e:
                    logger.error(f"Ошибка остановки PageKite: {e}")
                    try:
                        self.pagekite_process.kill()
                        logger.info("✅ PageKite принудительно остановлен")
                    except Exception as e2:
                        logger.error(f"Ошибка принудительной остановки PageKite: {e2}")
            
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
    print("🌐 С webhook сервером и PageKite")
    print("=" * 50)
    
    app_manager = ApplicationManager()
    app_manager.start()

if __name__ == "__main__":
    main()
