import sqlite3
import datetime
from typing import Optional, List, Tuple
from config import DATABASE_PATH

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_PATH)
        self.create_tables()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Таблица пользователей
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Таблица подписок
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS subscriptions (
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
        
        # Таблица платежей
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                payment_id TEXT UNIQUE,
                amount INTEGER,
                status TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        # Таблица администраторов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS admins (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                role TEXT DEFAULT 'admin',
                added_by INTEGER,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1,
                FOREIGN KEY (user_id) REFERENCES users (user_id),
                FOREIGN KEY (added_by) REFERENCES admins (user_id)
            )
        ''')
        
        self.conn.commit()
    
    def add_user(self, user_id: int, username: str = None, first_name: str = None, last_name: str = None):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO users (user_id, username, first_name, last_name)
            VALUES (?, ?, ?, ?)
        ''', (user_id, username, first_name, last_name))
        self.conn.commit()
    
    def get_user(self, user_id: int) -> Optional[Tuple]:
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        return cursor.fetchone()
    
    def get_all_users(self) -> List[Tuple]:
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users ORDER BY joined_at DESC')
        return cursor.fetchall()
    
    def create_subscription(self, user_id: int, payment_id: str, amount: int, duration_days: int = 30):
        cursor = self.conn.cursor()
        start_date = datetime.datetime.now()
        end_date = start_date + datetime.timedelta(days=duration_days)
        
        # Деактивируем предыдущие подписки
        cursor.execute('UPDATE subscriptions SET is_active = 0 WHERE user_id = ?', (user_id,))
        
        # Создаем новую подписку
        cursor.execute('''
            INSERT INTO subscriptions (user_id, payment_id, amount, start_date, end_date, is_active)
            VALUES (?, ?, ?, ?, ?, 1)
        ''', (user_id, payment_id, amount, start_date, end_date))
        
        self.conn.commit()
        return cursor.lastrowid
    
    def get_active_subscription(self, user_id: int) -> Optional[Tuple]:
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM subscriptions 
            WHERE user_id = ? AND is_active = 1 AND end_date > datetime('now')
        ''', (user_id,))
        return cursor.fetchone()
    
    def get_expiring_subscriptions(self, days_before: int = 3) -> List[Tuple]:
        cursor = self.conn.cursor()
        future_date = datetime.datetime.now() + datetime.timedelta(days=days_before)
        cursor.execute('''
            SELECT s.*, u.username, u.first_name 
            FROM subscriptions s
            JOIN users u ON s.user_id = u.user_id
            WHERE s.is_active = 1 
            AND s.end_date BETWEEN datetime('now') AND ?
            ORDER BY s.end_date
        ''', (future_date,))
        return cursor.fetchall()
    
    def get_expired_subscriptions(self) -> List[Tuple]:
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT s.*, u.username, u.first_name 
            FROM subscriptions s
            JOIN users u ON s.user_id = u.user_id
            WHERE s.is_active = 1 AND s.end_date <= datetime('now')
            ORDER BY s.end_date
        ''')
        return cursor.fetchall()
    
    def deactivate_subscription(self, user_id: int):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE subscriptions SET is_active = 0 WHERE user_id = ?', (user_id,))
        self.conn.commit()
    
    def add_payment(self, user_id: int, payment_id: str, amount: int, status: str):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO payments (user_id, payment_id, amount, status)
            VALUES (?, ?, ?, ?)
        ''', (user_id, payment_id, amount, status))
        self.conn.commit()
    
    def get_payments_report(self, start_date: str, end_date: str) -> List[Tuple]:
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT p.*, u.username, u.first_name, s.end_date
            FROM payments p
            JOIN users u ON p.user_id = u.user_id
            LEFT JOIN subscriptions s ON p.user_id = s.user_id AND p.payment_id = s.payment_id
            WHERE p.created_at BETWEEN ? AND ? AND p.status = 'success'
            ORDER BY p.created_at DESC
        ''', (start_date, end_date))
        return cursor.fetchall()
    
    def get_total_payments_amount(self, start_date: str, end_date: str) -> int:
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT SUM(amount) FROM payments 
            WHERE created_at BETWEEN ? AND ? AND status = 'success'
        ''', (start_date, end_date))
        result = cursor.fetchone()
        return result[0] if result[0] else 0
    
    def get_users_with_active_subscriptions(self) -> List[Tuple]:
        """Получить пользователей с активными подписками"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT s.*, u.username, u.first_name, u.last_name
            FROM subscriptions s
            JOIN users u ON s.user_id = u.user_id
            WHERE s.is_active = 1 AND s.end_date > datetime('now')
            ORDER BY s.end_date DESC
        ''')
        return cursor.fetchall()
    
    def get_users_with_expired_subscriptions(self) -> List[Tuple]:
        """Получить пользователей с истекшими подписками"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT s.*, u.username, u.first_name, u.last_name
            FROM subscriptions s
            JOIN users u ON s.user_id = u.user_id
            WHERE s.is_active = 1 AND s.end_date <= datetime('now')
            ORDER BY s.end_date DESC
        ''')
        return cursor.fetchall()
    
    def is_admin(self, user_id: int) -> bool:
        """Проверить, является ли пользователь администратором"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT is_active FROM admins WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        return result is not None and result[0] == 1
    
    def add_admin(self, user_id: int, username: str = None, first_name: str = None, 
                  last_name: str = None, role: str = 'admin', added_by: int = None):
        """Добавить администратора"""
        cursor = self.conn.cursor()
        
        # Сначала добавляем пользователя в таблицу users, если его там нет
        self.add_user(user_id, username, first_name, last_name)
        
        # Добавляем в таблицу администраторов
        cursor.execute('''
            INSERT OR REPLACE INTO admins (user_id, username, first_name, last_name, role, added_by, is_active)
            VALUES (?, ?, ?, ?, ?, ?, 1)
        ''', (user_id, username, first_name, last_name, role, added_by))
        
        self.conn.commit()
        return cursor.lastrowid
    
    def remove_admin(self, user_id: int):
        """Удалить администратора (деактивировать)"""
        cursor = self.conn.cursor()
        cursor.execute('UPDATE admins SET is_active = 0 WHERE user_id = ?', (user_id,))
        self.conn.commit()
    
    def get_all_admins(self) -> List[Tuple]:
        """Получить всех активных администраторов"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM admins 
            WHERE is_active = 1 
            ORDER BY added_at DESC
        ''')
        return cursor.fetchall()
    
    def get_admin_info(self, user_id: int) -> Optional[Tuple]:
        """Получить информацию об администраторе"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM admins WHERE user_id = ? AND is_active = 1', (user_id,))
        return cursor.fetchone()
    
    def update_admin_role(self, user_id: int, role: str):
        """Обновить роль администратора"""
        cursor = self.conn.cursor()
        cursor.execute('UPDATE admins SET role = ? WHERE user_id = ?', (role, user_id))
        self.conn.commit()
    
    def close(self):
        self.conn.close()
