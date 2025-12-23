import os
from log import log 

def cat(st):
    
    if len(st) == 1: # Проверка количества аргументов
        print("Ошибка: не указан файл для чтения")
        log("cat", success = False, error = "No file specified")
        return

    path = st[1]   # Путь к файлу (первый аргумент после команды)
    command = ' '.join(st)  # собираем команду для логирования

    try:
        # Проверка существования файла
        if not os.path.exists(path):
            raise FileNotFoundError('No such file or directory')
        
        # Проверка, что путь ведет к файлу, а не к директории
        if os.path.isdir(path):
            raise IsADirectoryError('Is a directory')

        # Открытие и чтение файла
        with open(path, 'r', encoding = 'utf-8') as file:
            print(file.read())  # Вывод содержимого файла в консоль

        # Логирование успешного выполнения
        log(command, success = True) 

    except Exception as e:
        # Обработка ошибок при чтении файла
        print(f"Ошибка: не удалось прочитать '{path}' — {e}") 
        # Логирование ошибки
        log(command, success = False, error = str(e))