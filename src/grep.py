import os
import re

def grep(st):
    # st: массив вида ["grep", "pattern", "path"] или ["grep", "-r", "-i", "pattern", "path"]

    recursive = False     # флаг рекурсивного поиска
    ignore_case = False   # флаг игнорирования регистра
    pattern = None        # шаблон для поиска
    path = None           # путь к файлу или каталогу

    # разбор аргументов
    for t in st[1:]:
        if t == '-r':
            recursive = True
        elif t == '-i':
            ignore_case = True
        elif pattern is None:
            pattern = t
        elif path is None:
            path = t

    # проверка на наличие обязательных аргументов
    if not pattern or not path:
        print("Ошибка: недостаточно аргументов. Использование: grep [-r] [-i] pattern path")
        return

    # настройка регулярного выражения
    flags = re.IGNORECASE if ignore_case else 0
    regex = re.compile(pattern, flags)

    # проверка существования пути
    if not os.path.exists(path):
        print(f"Ошибка: путь '{path}' не найден.")
        return

    # если путь — файл
    if os.path.isfile(path):
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                for num, line in enumerate(f, start=1):
                    if regex.search(line):
                        print(f"{path}:{num}: {line.strip()}")
        except Exception as e:
            print(f"Ошибка при чтении файла '{path}': {e}")
        return

    # если путь — каталог
    for root, dirs, files in os.walk(path):
        for name in files:
            file_path = os.path.join(root, name)
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    for num, line in enumerate(f, start=1):
                        if regex.search(line):
                            print(f"{file_path}:{num}: {line.strip()}")
            except Exception as e:
                print(f"Ошибка при чтении файла '{file_path}': {e}")

        # если не рекурсивный поиск — выходим после первого уровня
        if not recursive:
            break
