#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Обновление схемы базы данных для добавления контактных данных
"""

import sqlite3
import os
from config import DATABASE_PATH

def update_database_schema():
    """Обновление схемы базы данных"""
    
    print("🔧 ОБНОВЛЕНИЕ СХЕМЫ БАЗЫ ДАННЫХ")
    print("=" * 50)
    
    # Создаем резервную копию
    if os.path.exists(DATABASE_PATH):
        backup_path = f"{DATABASE_PATH}.backup"
        os.rename(DATABASE_PATH, backup_path)
        print(f"💾 Создана резервная копия: {backup_path}")
    
    # Подключаемся к базе данных
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    try:
        # Проверяем существующие колонки в таблице users
        cursor.execute("PRAGMA table_info(users)")
        columns = cursor.fetchall()
        existing_columns = [col[1] for col in columns]
        
        print(f"📋 Существующие колонки: {existing_columns}")
        
        # Добавляем колонку phone если её нет
        if 'phone' not in existing_columns:
            cursor.execute("ALTER TABLE users ADD COLUMN phone TEXT")
            print("✅ Добавлена колонка 'phone'")
        else:
            print("ℹ️ Колонка 'phone' уже существует")
        
        # Добавляем колонку email если её нет
        if 'email' not in existing_columns:
            cursor.execute("ALTER TABLE users ADD COLUMN email TEXT")
            print("✅ Добавлена колонка 'email'")
        else:
            print("ℹ️ Колонка 'email' уже существует")
        
        # Сохраняем изменения
        conn.commit()
        
        # Проверяем обновленную схему
        cursor.execute("PRAGMA table_info(users)")
        updated_columns = cursor.fetchall()
        print(f"📋 Обновленные колонки: {[col[1] for col in updated_columns]}")
        
        print("✅ Схема базы данных успешно обновлена!")
        
    except Exception as e:
        print(f"❌ Ошибка обновления схемы: {e}")
        # Восстанавливаем резервную копию при ошибке
        if os.path.exists(f"{DATABASE_PATH}.backup"):
            os.rename(f"{DATABASE_PATH}.backup", DATABASE_PATH)
            print("🔄 Восстановлена резервная копия")
        raise
    
    finally:
        conn.close()

if __name__ == "__main__":
    update_database_schema()
