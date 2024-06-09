#!/bin/bash

# Проверяем, был ли передан аргумент
if [ $# -eq 0 ]; then
    echo "Usage: $0 <relative_path_to_file>"
    exit 1
fi

# Базовый URL для репозитория на GitHub
base_github_url="https://raw.githubusercontent.com/MagicBusX/pypkg-repo/main/"

# Относительный путь к файлу на GitHub
relative_path=$1

# Формирование полного URL файла на GitHub
github_file_url="$base_github_url$relative_path"

# Загрузка содержимого файла с GitHub
file_contents=$(curl -sSL "$github_file_url")

# Проверка, удалось ли загрузить файл
if [ -z "$file_contents" ]; then
    echo "Ошибка: не удалось загрузить файл с $github_file_url"
    exit 1
fi

# Построчное выполнение команд
while IFS= read -r line; do
    # Пропускаем пустые строки
    if [ -n "$line" ]; then
        # Выводим команду перед выполнением
        echo "Выполняется: $line"
        # Выполняем команду
        eval "$line"
        # Проверяем статус выполнения команды
        if [ $? -ne 0 ]; then
            echo "Ошибка выполнения команды: $line"
            exit 1
        fi
    fi
done <<< "$file_contents"
