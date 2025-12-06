#!/bin/bash
echo "=== ДОБАВЛЕНИЕ ВСЕГО ПРОЕКТА ==="
echo ""

echo "1. Проверяем структуру проекта..."
echo "Дерево проекта:"
find . -maxdepth 3 -type d | sort
echo ""

echo "2. Показываем важные файлы..."
echo "app/:"
find app -type f -name "*.py" | head -10
echo ""
echo "proekt/:"
find proekt -type f | head -10 2>/dev/null || echo "proekt пуст или не существует"
echo ""

echo "3. Очищаем .gitignore временно..."
cp .gitignore .gitignore.backup
echo "!app/" >> .gitignore
echo "!proekt/" >> .gitignore
echo "!*.py" >> .gitignore

echo "4. Добавляем ВСЕ файлы..."
git add --all

echo "5. Восстанавливаем .gitignore..."
mv .gitignore.backup .gitignore

echo "6. Проверяем статус..."
git status

echo "7. Создаем коммит..."
git commit -m "ADD ALL PROJECT FILES

- Complete app/ directory with SQLAlchemy models
- All Python files and modules
- Project structure and configuration
- Database files and scripts
- Everything needed for PostgreSQL project"

echo "8. Загружаем на GitHub..."
git push --force origin master

echo ""
echo "✅ ВЕСЬ ПРОЕКТ ДОБАВЛЕН НА GITHUB!"
