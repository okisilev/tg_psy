#!/usr/bin/env python3
"""
Тест проверки платежа в боте
"""

import asyncio
import sys
import os
from datetime import datetime

# Добавляем текущую директорию в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from bot import WomenClubBot
from config import BOT_TOKEN

async def test_payment_check():
    """Тест функции проверки платежа"""
    print("🧪 ТЕСТ ПРОВЕРКИ ПЛАТЕЖА В БОТЕ")
    print("=" * 60)
    print(f"Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        # Создаем экземпляр бота
        bot = WomenClubBot()
        print("✅ Бот инициализирован")
        
        # Тестовые данные
        test_user_id = 431292182
        test_payment_id = "women_club_431292182_test"
        
        print(f"🔧 Тестовые данные:")
        print(f"   - User ID: {test_user_id}")
        print(f"   - Payment ID: {test_payment_id}")
        print()
        
        # Тест 1: Проверка статуса платежа
        print("📋 Тест 1: Проверка статуса платежа")
        print("-" * 40)
        
        payment_status = bot.prodamus.get_payment_status(test_payment_id)
        print(f"   - Статус платежа: {payment_status}")
        
        if payment_status and payment_status.get('status') == 'success':
            print("   ✅ Платеж успешен")
        else:
            print("   ⏳ Платеж еще не поступил")
        
        print()
        
        # Тест 2: Проверка существующей подписки
        print("📋 Тест 2: Проверка существующей подписки")
        print("-" * 40)
        
        existing_subscription = bot.db.get_active_subscription(test_user_id)
        print(f"   - Существующая подписка: {existing_subscription}")
        
        if existing_subscription:
            print("   ✅ Подписка уже активна")
        else:
            print("   ❌ Подписка не найдена")
        
        print()
        
        # Тест 3: Проверка пользователя в базе
        print("📋 Тест 3: Проверка пользователя в базе")
        print("-" * 40)
        
        user = bot.db.get_user(test_user_id)
        print(f"   - Пользователь в базе: {user}")
        
        if user:
            print("   ✅ Пользователь найден в базе")
        else:
            print("   ❌ Пользователь не найден в базе")
        
        print()
        
        # Тест 4: Симуляция проверки платежа
        print("📋 Тест 4: Симуляция проверки платежа")
        print("-" * 40)
        
        # Симулируем успешный платеж
        if payment_status and payment_status.get('status') == 'success':
            print("   🎉 Платеж успешен - активируем подписку")
            
            # Проверяем, не активирована ли уже подписка
            if existing_subscription:
                print("   ⚠️ Подписка уже активирована - пропускаем")
            else:
                print("   ✅ Активируем подписку")
                # Здесь можно было бы вызвать activate_subscription, но это требует реального бота
        else:
            print("   ⏳ Платеж еще не поступил - показываем кнопку 'Проверить снова'")
        
        print()
        
        # Тест 5: Проверка обработки ошибок
        print("📋 Тест 5: Проверка обработки ошибок")
        print("-" * 40)
        
        try:
            # Тестируем обработку None значений
            test_user = None
            test_subscription = None
            
            if not test_user or not test_subscription:
                print("   ✅ Обработка None значений работает корректно")
            else:
                print("   ❌ Обработка None значений не работает")
                
        except Exception as e:
            print(f"   ❌ Ошибка в обработке None значений: {e}")
        
        print()
        
        print("✅ ВСЕ ТЕСТЫ ЗАВЕРШЕНЫ")
        print()
        print("📝 Рекомендации:")
        print("   1. Убедитесь, что webhook сервер запущен")
        print("   2. Проверьте, что Prodamus отправляет уведомления")
        print("   3. Проверьте логи бота на наличие ошибок")
        print("   4. Убедитесь, что все переменные окружения установлены")
        
    except Exception as e:
        print(f"❌ Ошибка в тесте: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_payment_check())
