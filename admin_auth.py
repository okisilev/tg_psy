"""
Модуль для работы с правами администраторов
"""
from typing import List, Optional
from database import Database
from config import ADMIN_CHAT_ID, ADMIN_IDS

class AdminAuth:
    def __init__(self, db: Database):
        self.db = db
        self._initialize_default_admins()
    
    def _initialize_default_admins(self):
        """Инициализация администраторов по умолчанию из конфигурации"""
        # Добавляем главного администратора из ADMIN_CHAT_ID
        if ADMIN_CHAT_ID:
            try:
                admin_id = int(ADMIN_CHAT_ID)
                if not self.db.is_admin(admin_id):
                    self.db.add_admin(admin_id, role='super_admin')
            except (ValueError, TypeError):
                pass
        
        # Добавляем администраторов из списка ADMIN_IDS
        for admin_id_str in ADMIN_IDS:
            try:
                admin_id = int(admin_id_str.strip())
                if not self.db.is_admin(admin_id):
                    self.db.add_admin(admin_id, role='admin')
            except (ValueError, TypeError):
                continue
    
    def is_admin(self, user_id: int) -> bool:
        """Проверить, является ли пользователь администратором"""
        return self.db.is_admin(user_id)
    
    def is_super_admin(self, user_id: int) -> bool:
        """Проверить, является ли пользователь супер-администратором"""
        admin_info = self.db.get_admin_info(user_id)
        return admin_info is not None and admin_info[4] == 'super_admin'  # role field
    
    def can_manage_admins(self, user_id: int) -> bool:
        """Проверить, может ли пользователь управлять администраторами"""
        return self.is_super_admin(user_id)
    
    def add_admin(self, user_id: int, username: str = None, first_name: str = None, 
                  last_name: str = None, role: str = 'admin', added_by: int = None) -> bool:
        """Добавить администратора"""
        if not self.can_manage_admins(added_by):
            return False
        
        try:
            self.db.add_admin(user_id, username, first_name, last_name, role, added_by)
            return True
        except Exception:
            return False
    
    def remove_admin(self, user_id: int, removed_by: int) -> bool:
        """Удалить администратора"""
        if not self.can_manage_admins(removed_by):
            return False
        
        # Нельзя удалить самого себя
        if user_id == removed_by:
            return False
        
        # Нельзя удалить супер-администратора
        if self.is_super_admin(user_id):
            return False
        
        try:
            self.db.remove_admin(user_id)
            return True
        except Exception:
            return False
    
    def get_all_admins(self) -> List[tuple]:
        """Получить всех администраторов"""
        return self.db.get_all_admins()
    
    def get_admin_info(self, user_id: int) -> Optional[tuple]:
        """Получить информацию об администраторе"""
        return self.db.get_admin_info(user_id)
    
    def update_admin_role(self, user_id: int, role: str, updated_by: int) -> bool:
        """Обновить роль администратора"""
        if not self.can_manage_admins(updated_by):
            return False
        
        # Нельзя изменить роль супер-администратора
        if self.is_super_admin(user_id):
            return False
        
        try:
            self.db.update_admin_role(user_id, role)
            return True
        except Exception:
            return False
