#!/bin/bash
echo "=== ИСПРАВЛЕНИЕ ВЕТКИ ==="
echo ""

echo "1. Текущая ветка:"
CURRENT_BRANCH=$(git branch --show-current)
echo "   $CURRENT_BRANCH"

echo ""
echo "2. Все локальные ветки:"
git branch

echo ""
echo "3. Все удаленные ветки:"
git branch -r

echo ""
echo "4. Добавляем ВСЕ файлы проекта..."
git add --all

echo ""
echo "5. Проверяем что добавилось..."
git status

echo ""
echo "6. Создаем коммит..."
git commit -m "COMPLETE PROJECT: PostgreSQL SQLAlchemy

- app/ directory with all Python files
- Database models and CRUD operations
- Project configuration files
- Complete structure"

echo ""
echo "7. Загружаем в правильную ветку ($CURRENT_BRANCH)..."
git push origin $CURRENT_BRANCH

echo ""
echo "✅ Проект загружен в ветку: $CURRENT_BRANCH"
echo "�� Ссылка: https://github.com/gabrielakazaku/praktikabot/tree/$CURRENT_BRANCH"
