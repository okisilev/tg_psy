#!/usr/bin/env python3
"""
Скрипт для инициализации администраторов в базе данных
"""
import os
import sys
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Добавляем текущую директорию в путь для импорта модулей
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import Database
from admin_auth import AdminAuth

def main():
    """Инициализация администраторов"""
    print("🔧 Инициализация администраторов...")
    
    # Создаем подключение к базе данных
    db = Database()
    admin_auth = AdminAuth(db)
    
    # Получаем ID администраторов из переменных окружения
    admin_chat_id = os.getenv('ADMIN_CHAT_ID')
    admin_ids = os.getenv('ADMIN_IDS', '').split(',') if os.getenv('ADMIN_IDS') else []
    
    print(f"📋 Найдено администраторов в конфигурации: {len(admin_ids) + (1 if admin_chat_id else 0)}")
    
    # Добавляем главного администратора
    if admin_chat_id:
        try:
            admin_id = int(admin_chat_id)
            if not admin_auth.is_admin(admin_id):
                admin_auth.add_admin(admin_id, role='super_admin')
                print(f"✅ Главный администратор {admin_id} добавлен как супер-администратор")
            else:
                print(f"ℹ️  Главный администратор {admin_id} уже существует")
        except (ValueError, TypeError) as e:
            print(f"❌ Ошибка добавления главного администратора: {e}")
    
    # Добавляем остальных администраторов
    for admin_id_str in admin_ids:
        try:
            admin_id = int(admin_id_str.strip())
            if not admin_auth.is_admin(admin_id):
                admin_auth.add_admin(admin_id, role='admin')
                print(f"✅ Администратор {admin_id} добавлен")
            else:
                print(f"ℹ️  Администратор {admin_id} уже существует")
        except (ValueError, TypeError) as e:
            print(f"❌ Ошибка добавления администратора {admin_id_str}: {e}")
    
    # Показываем список всех администраторов
    print("\n📊 Текущие администраторы:")
    admins = admin_auth.get_all_admins()
    if admins:
        for admin in admins:
            username = f"@{admin[1]}" if admin[1] else f"ID:{admin[0]}"
            role = admin[4] or "admin"
            print(f"  • {username} - {role}")
    else:
        print("  📭 Администраторов не найдено")
    
    print("\n✅ Инициализация завершена!")
    
    # Закрываем соединение с базой данных
    db.close()

if __name__ == "__main__":
    main()
