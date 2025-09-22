
# 📦 РУКОВОДСТВО ПО УСТАНОВКЕ PAGKITE

## ❌ Проблема с pip

PageKite не доступен через pip, поэтому нужно скачивать его напрямую.

## 🚀 Способы установки

### Способ 1: Автоматическая установка

```bash
# Запуск скрипта установки
./install_pagekite.sh
```

### Способ 2: Ручная установка

```bash
# Скачивание PageKite
wget https://pagekite.net/pk/pagekite.py

# Установка прав доступа
chmod +x pagekite.py

# Проверка установки
./pagekite.py --help
```

### Способ 3: Альтернативное скачивание

```bash
# Если wget не работает
curl -O https://pagekite.net/pk/pagekite.py
chmod +x pagekite.py
```

## 🔧 Настройка

### 1. Установка PageKite

```bash
# Запуск скрипта установки
./install_pagekite.sh
```

### 2. Запуск с PageKite

```bash
# Запуск webhook с PageKite
./start_pagekite_webhook.sh
```

### 3. Простой запуск (без PageKite)

```bash
# Запуск только webhook сервера
./start_webhook_simple.sh
```

## 🧪 Тестирование

### 1. Проверка PageKite

```bash
# Проверка работы PageKite
./pagekite.py --help
```

### 2. Тест webhook

```bash
# Тест локального webhook
curl http://localhost:5000/health

# Тест через PageKite (если настроен)
curl https://dashastar.pagekite.me/health
```

## ⚠️ Альтернативы PageKite

### 1. Простой webhook (HTTP)

```bash
# Запуск без PageKite
./start_webhook_simple.sh
```

**Настройки для Prodamus:**
- URL: `http://82.147.71.244:5000/sales/prodamus`
- Метод: POST
- Заголовки: `Sign: {signature}`

### 2. Ngrok (альтернатива PageKite)

```bash
# Установка ngrok
wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip
unzip ngrok-stable-linux-amd64.zip
chmod +x ngrok

# Запуск ngrok
./ngrok http 5000
```

### 3. SSH туннель

```bash
# Создание SSH туннеля
ssh -R 80:localhost:5000 serveo.net
```

## 🔧 Управление сервисами

### Запуск

```bash
# С PageKite
./start_pagekite_webhook.sh

# Без PageKite
./start_webhook_simple.sh
```

### Остановка

```bash
# Остановка всех сервисов
./stop_pagekite_webhook.sh

# Или вручную
pkill -f webhook_http.py
pkill -f pagekite.py
```

### Проверка статуса

```bash
# Проверка процессов
ps aux | grep -E "(webhook_http.py|pagekite.py)"

# Проверка портов
netstat -tlnp | grep :5000
```

## 🚨 Устранение неполадок

### Проблема: PageKite не скачивается

**Решение:**
```bash
# Попробуйте curl вместо wget
curl -O https://pagekite.net/pk/pagekite.py

# Или скачайте вручную и загрузите на сервер
```

### Проблема: PageKite не запускается

**Решение:**
```bash
# Проверьте права доступа
chmod +x pagekite.py

# Проверьте Python
python3 pagekite.py --help
```

### Проблема: Webhook не отвечает

**Решение:**
```bash
# Используйте простой webhook
./start_webhook_simple.sh

# Проверьте работу
curl http://localhost:5000/health
```

## 📝 Рекомендации

### 1. Для тестирования

Используйте простой webhook без PageKite:
```bash
./start_webhook_simple.sh
```

### 2. Для продакшена

Настройте VPS с публичным IP и SSL сертификатом.

### 3. Для разработки

Используйте ngrok или SSH туннель.

---

**Выберите подходящий способ установки PageKite или используйте альтернативы! 🚀**
