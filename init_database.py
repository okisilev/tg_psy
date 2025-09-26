#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Инициализация базы данных с полной схемой
"""

import sqlite3
import os
from config import DATABASE_PATH

def init_database():
    """Инициализация базы данных"""
    
    print("🔧 ИНИЦИАЛИЗАЦИЯ БАЗЫ ДАННЫХ")
    print("=" * 50)
    
    # Удаляем старую базу данных если существует
    if os.path.exists(DATABASE_PATH):
        os.remove(DATABASE_PATH)
        print(f"🗑️ Удалена старая база данных: {DATABASE_PATH}")
    
    # Подключаемся к базе данных
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    try:
        # Создаем таблицу пользователей с контактными данными
        cursor.execute('''
            CREATE TABLE users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                phone TEXT,
                email TEXT,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("✅ Создана таблица 'users' с контактными данными")
        
        # Создаем таблицу подписок
        cursor.execute('''
            CREATE TABLE subscriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                payment_id TEXT,
                amount INTEGER,
                start_date TIMESTAMP,
                end_date TIMESTAMP,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        print("✅ Создана таблица 'subscriptions'")
        
        # Создаем таблицу платежей
        cursor.execute('''
            CREATE TABLE payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                payment_id TEXT UNIQUE,
                amount INTEGER,
                status TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        print("✅ Создана таблица 'payments'")
        
        # Создаем таблицу администраторов
        cursor.execute('''
            CREATE TABLE admins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                role TEXT DEFAULT 'admin',
                added_by INTEGER,
                is_active BOOLEAN DEFAULT 1,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id),
                FOREIGN KEY (added_by) REFERENCES users (user_id)
            )
        ''')
        print("✅ Создана таблица 'admins'")
        
        # Сохраняем изменения
        conn.commit()
        
        # Проверяем созданные таблицы
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"📋 Созданные таблицы: {[table[0] for table in tables]}")
        
        # Проверяем схему таблицы users
        cursor.execute("PRAGMA table_info(users)")
        columns = cursor.fetchall()
        print(f"📋 Колонки таблицы users: {[col[1] for col in columns]}")
        
        print("✅ База данных успешно инициализирована!")
        
    except Exception as e:
        print(f"❌ Ошибка инициализации базы данных: {e}")
        raise
    
    finally:
        conn.close()

if __name__ == "__main__":
    init_database()
