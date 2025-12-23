import shutil  
import os  
import time   
from log import log 

# Директория для корзины (удаленные файлы перемещаются сюда)
TRASH_DIR = ".trash"  

# Создаем директорию корзины, если она не существует
os.makedirs(TRASH_DIR, exist_ok=True)

def rm(st):
    recur = ''  # Флаг рекурсивного удаления (-r)
    path = ''   # Путь к удаляемому объекту

    # Проверка наличия необходимых аргументов
    if len(st) < 2:
        print("Ошибка: не указан путь для удаления")
        log(" ".join(st), success = False, error = "No path specified")
        return

    # Обработка флага рекурсивного удаления
    if st[1] == '-r': 
        recur = '-r'
        if len(st) < 3:
            # Проверка наличия пути после флага -r
            print("Ошибка: не указан каталог для рекурсивного удаления")
            log(" ".join(st), success = False, error = "No directory specified for recursive delete")
            return
        path = st[2]
    else:
        path = st[1]

    command = ' '.join(st)  # Полная команда для логирования

    # Защита от удаления системных директорий
    if path in ['/', '..']:
        error = 'Удаление запрещено: корневой или родительский каталог'
        print(f'Ошибка:Удаление запрещено: корневой или родительский каталог')
        log(command, success = False, error = error)
        return

    try:
        # Проверка существования удаляемого объекта
        if not os.path.exists(path):
            raise FileNotFoundError('Файл или каталог не существует')

        # Удаление директории
        if os.path.isdir(path):
            if recur == '': 
                # Ошибка: попытка удалить директорию без флага -r
                raise IsADirectoryError('Это каталог. Используйте -r для рекурсивного удаления')
            elif recur == '-r':  
                # Запрос подтверждения для рекурсивного удаления директории
                confirm = input(f"Вы уверены, что хотите удалить каталог '{path}' и всё его содержимое? (y/n): ")
                if confirm.lower() != 'y': 
                    print('Удаление отменено.')
                    log(command, success = False, error = 'Удаление отменено пользователем')
                    return

                # Формирование пути в корзине для директории
                trash_path = os.path.join(TRASH_DIR, os.path.basename(path))

                # Если файл с таким именем уже есть в корзине - добавляем временную метку
                if os.path.exists(trash_path):
                    trash_path = os.path.join(TRASH_DIR, f"{os.path.basename(path)}_{int(time.time())}")
                
                # Перемещение директории в корзину
                shutil.move(path, trash_path)
        else:
            # Удаление файла
            # Формирование пути в корзине для файла
            trash_path = os.path.join(TRASH_DIR, os.path.basename(path))
            
            # Если файл с таким именем уже есть в корзине - добавляем временную метку
            if os.path.exists(trash_path):
                trash_path = os.path.join(TRASH_DIR, f"{os.path.basename(path)}_{int(time.time())}")
            
            # Перемещение файла в корзину
            shutil.move(path, trash_path)

        # Сообщение об успешном удалении
        print(f'Удалено: {path}')  
        log(command, success = True) 

    except Exception as e:
        # Обработка ошибок при удалении
        print(f"Ошибка: не удалось удалить '{path}' — {e}")  
        log(command, success = False, error = str(e))