# 🌐 РУКОВОДСТВО ПО ЗАМЕНЕ ДОМЕНА

## 📋 Где заменить `yourdomain.com` на реальный домен

### 1. Переменные окружения (ОСНОВНОЕ)

```bash
# Замените в терминале:
export WEBHOOK_URL="https://ВАШ_ДОМЕН.com/webhook/telegram"
export PRODAMUS_WEBHOOK_URL="https://ВАШ_ДОМЕН.com/webhook/prodamus"
```

### 2. Файл .env

```bash
# Отредактируйте файл .env:
WEBHOOK_URL=https://ВАШ_ДОМЕН.com/webhook/telegram
PRODAMUS_WEBHOOK_URL=https://ВАШ_ДОМЕН.com/webhook/prodamus
```

### 3. Файл config.py

```python
# В файле config.py найдите строки:
WEBHOOK_URL = os.getenv('WEBHOOK_URL', 'https://ВАШ_ДОМЕН.com/webhook/telegram')
PRODAMUS_WEBHOOK_URL = os.getenv('PRODAMUS_WEBHOOK_URL', 'https://ВАШ_ДОМЕН.com/webhook/prodamus')
```

## 🚀 Быстрая замена

### Вариант 1: Ручная замена

```bash
# 1. Установите переменные окружения
export WEBHOOK_URL="https://mydomain.com/webhook/telegram"
export PRODAMUS_WEBHOOK_URL="https://mydomain.com/webhook/prodamus"

# 2. Обновите .env файл
sed -i 's/yourdomain.com/mydomain.com/g' .env

# 3. Обновите config.py
sed -i 's/yourdomain.com/mydomain.com/g' config.py

# 4. Проверьте конфигурацию
python3 check_config.py
```

### Вариант 2: Использование скрипта

```bash
# Сделайте скрипт исполняемым
chmod +x replace_domain.sh

# Запустите замену
./replace_domain.sh mydomain.com
```

## 📝 Примеры доменов

### Локальная разработка:
```bash
export WEBHOOK_URL="https://localhost:5000/webhook/telegram"
export PRODAMUS_WEBHOOK_URL="https://localhost:5000/webhook/prodamus"
```

### Тестовый домен:
```bash
export WEBHOOK_URL="https://test.example.com/webhook/telegram"
export PRODAMUS_WEBHOOK_URL="https://test.example.com/webhook/prodamus"
```

### Продакшн домен:
```bash
export WEBHOOK_URL="https://mycompany.com/webhook/telegram"
export PRODAMUS_WEBHOOK_URL="https://mycompany.com/webhook/prodamus"
```

## 🔍 Проверка замены

После замены запустите:

```bash
# Проверка конфигурации
python3 check_config.py

# Тест создания платежа
python3 test_payment_creation.py

# Запуск webhook сервера
python3 start_webhook.py
```

## ⚠️ Важные замечания

### 1. SSL сертификат
- Убедитесь, что у вас есть SSL сертификат для домена
- Используйте Let's Encrypt для бесплатного SSL
- Проверьте, что домен доступен по HTTPS

### 2. Настройка Nginx/Apache
- Настройте проксирование на порт 5000
- Убедитесь, что webhook URL доступны
- Проверьте логи веб-сервера

### 3. Настройка в панели Prodamus
- Войдите в панель управления Prodamus
- Установите webhook URL: `https://ВАШ_ДОМЕН.com/webhook/prodamus`
- Включите демо-режим для тестирования

## 🧪 Тестирование

### 1. Проверка доступности
```bash
# Проверьте, что домен доступен
curl https://ВАШ_ДОМЕН.com/health

# Проверьте webhook
curl -X POST https://ВАШ_ДОМЕН.com/webhook/prodamus \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'
```

### 2. Тест платежа
```bash
# Создайте тестовый платеж
python3 test_payment_creation.py

# Откройте URL платежа в браузере
# Используйте тестовые карты для оплаты
```

## 📞 Поддержка

Если возникли проблемы:

1. **Проверьте конфигурацию**: `python3 check_config.py`
2. **Проверьте логи**: `python3 start_webhook.py`
3. **Проверьте доступность домена**: `curl https://ВАШ_ДОМЕН.com`
4. **Проверьте SSL сертификат**: `openssl s_client -connect ВАШ_ДОМЕН.com:443`

---

**Домен настроен! 🚀**
