import shutil 
import os     
from log import log  

def cp(st):
    # st - список аргументов команды (первый элемент - сама команда 'cp')
    
    recur = ''   # Флаг рекурсивного копирования (-r)
    what = ''    # Что копировать 
    where = ''   # Куда копировать

    # Обработка аргументов команды
    if len(st) > 1 and st[1] == '-r':
        # Рекурсивное копирование с флагом -r
        recur = '-r'
        if len(st) < 4: 
            # Проверка наличия всех необходимых аргументов
            print("Ошибка: недостаточно аргументов для рекурсивного копирования")
            log(" ".join(st), success=False, error="Not enough arguments for recursive copy")
            return
        what = st[2]    # Источник после флага -r
        where = st[3]   # Цель после флага -r
    else:
        # Обычное копирование без флага -r
        if len(st) < 3:
            # Проверка наличия всех необходимых аргументов
            print("Ошибка: недостаточно аргументов для копирования")
            log(" ".join(st), success=False, error="Not enough arguments")
            return
        what = st[1]    # Источник
        where = st[2]   # Цель

    command = ' '.join(st)  # Полная команда для логирования

    try:
        # Проверка существования источника
        if not os.path.exists(what):
            raise FileNotFoundError('Source does not exist')

        # Копирование в зависимости от типа источника
        if os.path.isdir(what):
            # Источник - директория
            if recur == '-r':
                # Рекурсивное копирование директории со всем содержимым
                shutil.copytree(what, where)
            else: 
                # Ошибка: копирование директории без флага -r
                raise IsADirectoryError('Source is a directory. Use -r for recursive copy')
        else:
            # Источник - файл
            shutil.copy2(what, where)  # copy2 сохраняет метаданные

        # Успешное завершение операции
        print(f'Успешно скопировано: {what} {where}') 
        log(command, success=True) 

    except Exception as e: 
        # Обработка ошибок при копировании
        print(f"Ошибка: не удалось скопировать '{what}' '{where}' — {e}") 
        log(command, success=False, error=str(e))