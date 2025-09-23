#!/bin/bash

# 📥 УСТАНОВКА PAGKITE
# Установка и настройка PageKite для webhook

echo "📥 УСТАНОВКА PAGKITE"
echo "=" * 50

# 1. Проверка наличия pagekite.py
echo "🔍 Проверка наличия pagekite.py..."
if [ -f "pagekite.py" ]; then
    echo "   ✅ pagekite.py уже установлен"
else
    echo "   📥 Скачивание pagekite.py..."
    wget -O pagekite.py https://pagekite.net/pk/pagekite.py
    if [ $? -eq 0 ]; then
        echo "   ✅ pagekite.py скачан"
        chmod +x pagekite.py
        echo "   ✅ pagekite.py сделан исполняемым"
    else
        echo "   ❌ Ошибка скачивания pagekite.py"
        echo "   🔧 Попробуйте альтернативный способ..."
        
        # Альтернативный способ скачивания
        curl -o pagekite.py https://pagekite.net/pk/pagekite.py
        if [ $? -eq 0 ]; then
            echo "   ✅ pagekite.py скачан через curl"
            chmod +x pagekite.py
            echo "   ✅ pagekite.py сделан исполняемым"
        else
            echo "   ❌ Ошибка скачивания через curl"
            echo "   📋 Проверьте интернет соединение"
            exit 1
        fi
    fi
fi

# 2. Проверка Python
echo "🐍 Проверка Python..."
python3 --version
if [ $? -eq 0 ]; then
    echo "   ✅ Python3 доступен"
else
    echo "   ❌ Python3 не найден"
    exit 1
fi

# 3. Тестирование PageKite
echo "🧪 Тестирование PageKite..."
echo "   - Запуск тестового подключения..."
timeout 10 ./pagekite.py 5000 dashastar.pagekite.me --help
if [ $? -eq 0 ]; then
    echo "   ✅ PageKite работает"
else
    echo "   ⚠️ PageKite не отвечает на --help"
    echo "   🔧 Это может быть нормально, если нет интернета"
fi

# 4. Создание скрипта запуска
echo "📝 Создание скрипта запуска..."
cat > start_pagekite.sh << 'EOF'
#!/bin/bash
# Запуск PageKite для webhook

echo "🌐 Запуск PageKite..."
./pagekite.py 5000 dashastar.pagekite.me &
PAGKITE_PID=$!
echo "PageKite PID: $PAGKITE_PID"
echo "Для остановки: kill $PAGKITE_PID"
EOF

chmod +x start_pagekite.sh
echo "   ✅ Скрипт start_pagekite.sh создан"

# 5. Создание скрипта остановки
echo "📝 Создание скрипта остановки..."
cat > stop_pagekite.sh << 'EOF'
#!/bin/bash
# Остановка PageKite

echo "⏹️ Остановка PageKite..."
pkill -f pagekite.py
echo "✅ PageKite остановлен"
EOF

chmod +x stop_pagekite.sh
echo "   ✅ Скрипт stop_pagekite.sh создан"

echo ""
echo "🎉 PAGKITE УСТАНОВЛЕН!"
echo ""
echo "📝 Статус:"
echo "   - pagekite.py: установлен"
echo "   - start_pagekite.sh: создан"
echo "   - stop_pagekite.sh: создан"
echo ""
echo "🚀 Запуск:"
echo "   ./start_pagekite.sh"
echo "   python3 main_with_pagekite.py"
echo ""
echo "🛑 Остановка:"
echo "   ./stop_pagekite.sh"
echo ""
echo "🧪 Тестирование:"
echo "   curl https://dashastar.pagekite.me/health"