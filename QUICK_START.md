# 🚀 Быстрый старт системы платежей Prodamus

## ✅ Система настроена и готова к работе!

### 📋 Что уже сделано:
- ✅ Конфигурация Prodamus настроена
- ✅ API интеграция реализована
- ✅ Webhook обработка настроена
- ✅ Демо-режим включен
- ✅ Тестовые карты подготовлены

## 🔧 Запуск системы

### 1. Установка зависимостей (опционально)
```bash
python3 install_dependencies.py
```

### 2. Проверка конфигурации
```bash
python3 simple_test.py
```

### 3. Запуск webhook сервера
```bash
python3 webhook.py
```

### 4. Тестирование платежей
Используйте тестовые карты для проверки:

#### 📱 Тестовые карты Сбербанка:
- **МИР**: `2202 2050 0001 2424` (05/35, CVC: 669)
- **MasterCard**: `5469 9801 0004 8525` (05/26, CVC: 041)
- **Visa**: `4006 8009 0096 2514` (05/26, CVC: 941)

#### 📱 Другие тестовые карты:
- **Монета**: `2200 2400 0000 0006` (12/24, CVC: 123)
- **ГазпромБанк**: `4242 4242 4242 4242` (12/30, CVC: 123)

## ⚙️ Конфигурация

### Основные параметры:
- **Shop ID**: `dashastar`
- **Secret Key**: `b2f9e8a399225271521dfe88a277a7371cb8c2cebfeaa6f0276ba81fcc303c93`
- **Demo Mode**: Включен
- **Webhook URL**: `https://--help/webhook/prodamus`

### Переменные окружения:
```bash
export PRODAMUS_SHOP_ID=dashastar
export PRODAMUS_SECRET_KEY=b2f9e8a399225271521dfe88a277a7371cb8c2cebfeaa6f0276ba81fcc303c93
export PRODAMUS_DEMO_MODE=true
export WEBHOOK_URL=https://--help/webhook/prodamus
```

## 🧪 Тестирование

### 1. Базовое тестирование:
```bash
python3 simple_test.py
```

### 2. Полное тестирование (требует зависимости):
```bash
python3 run_tests.py
```

### 3. Тестирование webhook:
```bash
python3 test_webhook.py
```

## 📁 Структура файлов

### Основные файлы:
- `config.py` - конфигурация системы
- `prodamus.py` - API интеграция с Prodamus
- `webhook.py` - обработчик webhook
- `smart_sender_integration.py` - интеграция с Smart Sender

### Тестовые файлы:
- `simple_test.py` - упрощенное тестирование
- `run_tests.py` - полное тестирование
- `test_prodamus_integration.py` - тест API
- `test_webhook.py` - тест webhook

### Документация:
- `PRODAMUS_SETUP_GUIDE.md` - подробное руководство
- `PRODAMUS_SETUP_REPORT.md` - отчет о настройке
- `QUICK_START.md` - данный файл

## 🚨 Устранение неполадок

### Проблема: ModuleNotFoundError
**Решение**: Установите зависимости:
```bash
pip install python-dotenv requests flask
```

### Проблема: Webhook не отвечает
**Решение**: Убедитесь, что сервер запущен:
```bash
python3 webhook.py
```

### Проблема: Ошибки API
**Решение**: Проверьте конфигурацию:
```bash
python3 simple_test.py
```

## 📞 Поддержка

При возникновении проблем:
1. Запустите `python3 simple_test.py` для диагностики
2. Проверьте логи системы
3. Убедитесь, что все зависимости установлены
4. Проверьте переменные окружения

## 🎯 Следующие шаги

1. **Настройка в панели Prodamus**:
   - Войти в панель управления
   - Настроить webhook URL
   - Включить демо-режим

2. **Тестирование платежей**:
   - Использовать тестовые карты
   - Проверить получение уведомлений
   - Протестировать обработку платежей

3. **Настройка Smart Sender**:
   - Получить API ключ
   - Настроить переменную `SMART_SENDER_API_KEY`
   - Протестировать интеграцию

---

**Система готова к работе! 🎉**
