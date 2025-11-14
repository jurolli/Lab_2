import shutil   # модуль для копирования файлов и директорий
import os       # модуль для работы с файловой системой
from log import log   # функция логирования

def cp(st):

    recur = ''   # флаг для рекурсивного копирования директорий
    what = ''    # источник (файл или папка)
    where = ''   # назначение (куда копировать)

    # разбор токенов
  # если второй токен — флаг "-r"
    if len(st) > 1 and st[1] == '-r':
        recur = '-r'
        if len(st) < 4:   # нужно минимум 4 токена: cp -r source dest
            print("Ошибка: недостаточно аргументов для рекурсивного копирования")
            log(" ".join(st), success=False, error="Not enough arguments for recursive copy")
            return
        what = st[2]
        where = st[3]
    else:
        # обычное копирование: cp source dest
        if len(st) < 3:
            print("Ошибка: недостаточно аргументов для копирования")
            log(" ".join(st), success=False, error="Not enough arguments")
            return
        what = st[1]
        where = st[2]

    command = ' '.join(st)   # собираем команду обратно в строку для логирования

    try:
        # проверяем, существует ли источник
        if not os.path.exists(what):
            raise FileNotFoundError('Source does not exist')

        # если источник — директория
        if os.path.isdir(what):
            if recur == '-r':   # рекурсивное копирование папки
                shutil.copytree(what, where)
            else:   # без флага -r копировать папку нельзя
                raise IsADirectoryError('Source is a directory. Use -r for recursive copy')
        else:
            # копирование файлаа
            shutil.copy2(what, where)

        print(f'Успешно скопировано: {what} {where}')   # сообщение об успехе
        log(command, success=True)   # логируем успешное выполнение

    except Exception as e:   # если возникла ошибка
        print(f"Ошибка: не удалось скопировать '{what}' '{where}' — {e}") 
        log(command, success=False, error=str(e))   # логируем неудачное выполнение 
