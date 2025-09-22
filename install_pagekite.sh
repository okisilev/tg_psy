#!/bin/bash

# 📦 УСТАНОВКА PAGKITE
# Скачивание и настройка PageKite

echo "📦 УСТАНОВКА PAGKITE"
echo "=" * 40

# 1. Проверка наличия PageKite
echo "🔍 Проверка наличия PageKite..."
if [ -f "pagekite.py" ]; then
    echo "   ✅ PageKite уже установлен"
    exit 0
fi

# 2. Скачивание PageKite
echo "📥 Скачивание PageKite..."
wget https://pagekite.net/pk/pagekite.py

if [ $? -eq 0 ]; then
    echo "   ✅ PageKite скачан успешно"
else
    echo "   ❌ Ошибка скачивания PageKite"
    echo "   🔧 Попробуйте альтернативный способ:"
    echo "      curl -O https://pagekite.net/pk/pagekite.py"
    exit 1
fi

# 3. Установка прав доступа
echo "🔐 Установка прав доступа..."
chmod +x pagekite.py

if [ $? -eq 0 ]; then
    echo "   ✅ Права доступа установлены"
else
    echo "   ❌ Ошибка установки прав доступа"
    exit 1
fi

# 4. Проверка установки
echo "🧪 Проверка установки..."
./pagekite.py --help

if [ $? -eq 0 ]; then
    echo "   ✅ PageKite установлен и работает"
else
    echo "   ❌ PageKite не работает"
    exit 1
fi

echo ""
echo "🎉 PAGKITE УСТАНОВЛЕН УСПЕШНО!"
echo ""
echo "📝 Использование:"
echo "   ./pagekite.py 5000 dashastar.pagekite.me"
echo ""
echo "🔧 Для запуска webhook с PageKite:"
echo "   ./start_pagekite_webhook.sh"
