# 🚀 Руководство по настройке и тестированию системы платежей Prodamus

## 📋 Обзор

Данное руководство поможет вам настроить и протестировать интеграцию с платежной системой Prodamus для Telegram бота "Женский клуб".

## 🔧 Настройка

### 1. Конфигурация Prodamus

#### Основные параметры:
- **Секретный ключ**: `b2f9e8a399225271521dfe88a277a7371cb8c2cebfeaa6f0276ba81fcc303c93`
- **Демо-режим**: Включен по умолчанию для тестирования
- **Webhook URL**: `https://yourdomain.com/webhook/prodamus`

#### Настройка в панели Prodamus:
1. Войдите в панель управления Prodamus
2. Перейдите в раздел "Настройки"
3. Включите демо-режим для тестирования
4. Настройте webhook URL для получения уведомлений

### 2. Переменные окружения

Создайте файл `.env` с следующими параметрами:

```bash
# Prodamus Configuration
PRODAMUS_SECRET_KEY=b2f9e8a399225271521dfe88a277a7371cb8c2cebfeaa6f0276ba81fcc303c93
PRODAMUS_DEMO_MODE=true

# Smart Sender Configuration
SMART_SENDER_API_KEY=your_smart_sender_api_key_here

# Webhook Configuration
WEBHOOK_URL=https://yourdomain.com/webhook/prodamus
```

## 🧪 Тестирование

### 1. Запуск тестов

```bash
# Запуск всех тестов
python run_tests.py

# Отдельные тесты
python test_prodamus_integration.py
python test_webhook.py
python smart_sender_integration.py
```

### 2. Тестовые карты

В демо-режиме используйте следующие тестовые карты:

#### Сбербанк:
- **МИР**: `2202 2050 0001 2424` (05/35, CVC: 669)
- **MasterCard**: `5469 9801 0004 8525` (05/26, CVC: 041)
- **Visa**: `4006 8009 0096 2514` (05/26, CVC: 941)

#### Другие банки:
- **Монета**: `2200 2400 0000 0006` (12/24, CVC: 123)
- **ГазпромБанк**: `4242 4242 4242 4242` (12/30, CVC: 123)

### 3. Проверка webhook

1. Запустите webhook сервер:
```bash
python webhook.py
```

2. Проверьте доступность:
```bash
curl http://localhost:5000/health
```

3. Протестируйте webhook:
```bash
python test_webhook.py
```

## 📊 API Методы Prodamus

### Основные методы:

1. **create_payment()** - Создание платежа
2. **get_payment_status()** - Получение статуса платежа
3. **set_activity()** - Установка активности заказа
4. **set_subscription_payment_date()** - Установка даты платежа подписки

### Пример использования:

```python
from prodamus import ProdаmusAPI

# Инициализация
prodamus = ProdаmusAPI()

# Создание платежа
payment = prodamus.create_payment(user_id=12345, username="test_user")
if payment:
    print(f"Payment URL: {payment['payment_url']}")

# Проверка статуса
status = prodamus.get_payment_status("order_123")
print(f"Status: {status}")
```

## 🔗 Интеграция с Smart Sender

### Настройка:

1. Получите API ключ Smart Sender
2. Установите переменную окружения `SMART_SENDER_API_KEY`
3. Протестируйте подключение:

```python
from smart_sender_integration import SmartSenderAPI

api = SmartSenderAPI()
if api.test_connection():
    print("Smart Sender подключен успешно!")
```

### Основные функции:

- **create_contact()** - Создание контакта
- **send_message()** - Отправка сообщения
- **add_to_sequence()** - Добавление в последовательность
- **update_contact()** - Обновление данных контакта

## 🚨 Устранение неполадок

### Частые проблемы:

1. **Ошибка подключения к API**
   - Проверьте правильность секретного ключа
   - Убедитесь, что демо-режим включен

2. **Webhook не получает уведомления**
   - Проверьте URL webhook в настройках Prodamus
   - Убедитесь, что сервер доступен извне
   - Проверьте логи webhook сервера

3. **Ошибки подписи**
   - Убедитесь, что используется правильный алгоритм HMAC-SHA256
   - Проверьте порядок параметров в строке подписи

### Логи и отладка:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Включите подробное логирование
logger = logging.getLogger(__name__)
logger.debug("Debug message")
```

## 📈 Мониторинг

### Проверка статуса системы:

1. **Health Check**: `GET /health`
2. **Логи webhook**: Проверьте файлы логов
3. **База данных**: Проверьте записи о платежах

### Метрики для отслеживания:

- Количество успешных платежей
- Количество неудачных платежей
- Время обработки webhook
- Ошибки API

## 🔒 Безопасность

### Рекомендации:

1. **Никогда не коммитьте секретные ключи в репозиторий**
2. **Используйте HTTPS для webhook**
3. **Проверяйте подписи всех входящих webhook**
4. **Логируйте все операции с платежами**

### Проверка подписи webhook:

```python
def verify_webhook(data, signature):
    expected_signature = generate_signature(data)
    return hmac.compare_digest(signature, expected_signature)
```

## 📞 Поддержка

При возникновении проблем:

1. Проверьте логи системы
2. Запустите диагностические тесты
3. Обратитесь к документации Prodamus
4. Проверьте статус сервисов Prodamus

## 🎯 Следующие шаги

После успешного тестирования:

1. Отключите демо-режим для продакшена
2. Настройте мониторинг системы
3. Подготовьте план резервного копирования
4. Настройте уведомления об ошибках

---

**Удачного тестирования! 🚀**
