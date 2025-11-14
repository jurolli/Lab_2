import shutil   # модуль для перемещения и копирования файлов/директорий
import os       # модуль для работы с файловой системой
from log import log   # функция логирования

def mv(st):


    # проверяем количество аргументов
    if len(st) < 3:
        print("Ошибка: недостаточно аргументов для перемещения")
        log(" ".join(st), success=False, error="Not enough arguments")
        return

    what = st[1]    # источник (файл или папка)
    where = st[2]   # назначение (куда перемещать)

    command = ' '.join(st)   # собираем команду обратно в строку для логирования

    try:
        # проверяем, существует ли источник
        if not os.path.exists(what):
            raise FileNotFoundError('Source does not exist')

        # если место назначения — директория, формируем полный путь
        if os.path.isdir(where):
            where = os.path.join(where, os.path.basename(what))

        # выполняем перемещение
        shutil.move(what, where)

        print(f'Успешно перемещено: {what} {where}')   # сообщение об успехе
        log(command, success=True)   # логируем успешное выполнение

    except Exception as e:   # если возникла ошибка
        print(f"Ошибка: не удалось переместить '{what}' '{where}' — {e}")   # выводим сообщение об ошибке
        log(command, success=False, error=str(e))   # логируем неудачное выполнение
