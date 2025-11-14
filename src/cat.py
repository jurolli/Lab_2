import os
from log import log

def cat(st):

    # если аргумент не указан, выводим ошибку
    if len(st) == 1:
        print("Ошибка: не указан файл для чтения")
        log("cat", success=False, error="No file specified")
        return

    path = st[1]   # берём путь из второго токена
    command = ' '.join(st)   # собираем команду обратно в строку для логирования

    try:
        # проверяем, существует ли путь
        if not os.path.exists(path):
            raise FileNotFoundError('No such file or directory')
        # проверяем, не является ли путь директорией
        if os.path.isdir(path):
            raise IsADirectoryError('Is a directory')

        # открываем файл в режиме чтения с кодировкой UTF-8
        with open(path, 'r', encoding='utf-8') as file:
            print(file.read())   # выводим содержимое файла

        log(command, success=True)   # логируем успешное выполнение команды

    except Exception as e:   # если возникла ошибка
        print(f"Ошибка: не удалось прочитать '{path}' — {e}")   # выводим сообщение об ошибке
        log(command, success=False, error=str(e))   # логируем неудачное выполнение
