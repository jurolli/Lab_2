import os
from log import log


def cd(st): 
    # Если аргументов нет - переходим в домашнюю директорию
    if len(st) == 1:
        path = os.path.expanduser('~')  # Получаем путь к домашней директории
    else:
        path = st[1]  # Берем путь из аргумента

    command = ' '.join(st)  # собираем команду для логирования

    try:
        # Обработка специальных случаев
        if path == '~':
            path = os.path.expanduser('~')  # Домашняя директория
        elif path == '..':
            # Переход на уровень выше
            path = os.path.abspath(os.path.join(os.getcwd(), '..'))

        # Выполнение смены рабочей директории
        os.chdir(path) 
        
        # Вывод текущей директории после перехода
        print(f"Перешли в каталог: {os.getcwd()}")
        
        # Логирование успешного выполнения
        log(command, success=True)

    except Exception as e:
        # Обработка ошибок при смене директории
        print(f"Ошибка: не удалось перейти в '{path}' — {e}")
        
        # Логирование ошибки
        log(command, success=False, error=str(e))

   