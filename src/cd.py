import os
from log import log


def cd(st):# если аргумент не указан, по умолчанию переходим в домашнюю директорию
    if len(st) == 1:
        path = os.path.expanduser('~')
    else:
        path = st[1]

    command = ' '.join(st)   # собираем команду обратно в строку для логирования

    try:
        # если путь равен "~", заменяем на домашнюю директорию пользователя
        if path == '~':
            path = os.path.expanduser('~')
        # если путь равен "..", переходим на уровень выше
        elif path == '..':
            path = os.path.abspath(os.path.join(os.getcwd(), '..'))

        os.chdir(path)   # меняем текущую рабочую директорию
        print(f"Перешли в каталог: {os.getcwd()}")   # выводим новый текущий каталог
        log(command, success=True)   # логируем успешное выполнение команды

    except Exception as e:   # если возникла ошибка
        print(f"Ошибка: не удалось перейти в '{path}' — {e}")   # выводим сообщение об ошибке
        log(command, success=False, error=str(e))   # логируем неудачное выполнение
   