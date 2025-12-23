import shutil   
import os     
from log import log  

def mv(st):
    """
    Функция для перемещения/переименования файлов и папок
    
    Параметры:
    st - список аргументов команды (первый элемент - сама команда 'mv')
    """
    
    # Проверка наличия необходимого количества аргументов
    if len(st) < 3:
        print("Ошибка: недостаточно аргументов для перемещения")
        log(" ".join(st), success=False, error="Not enough arguments")
        return

    what = st[1]   # Что перемещаем (источник)
    where = st[2]  # Куда перемещаем (цель)

    command = ' '.join(st)  # Полная команда для логирования

    try:
        # Проверка существования источника
        if not os.path.exists(what):
            raise FileNotFoundError('Source does not exist')

        # Если цель - директория, то перемещаем в эту директорию с сохранением имени
        if os.path.isdir(where):
            # Формируем полный путь: директория_назначения + имя_файла_источника
            where = os.path.join(where, os.path.basename(what))
        
        # Выполнение перемещения файла/папки
        shutil.move(what, where)

        # Вывод сообщения об успехе
        print(f'Успешно перемещено: {what} {where}') 
        # Логирование успешного выполнения
        log(command, success=True) 

    except Exception as e: 
        # Обработка ошибок при перемещении
        print(f"Ошибка: не удалось переместить '{what}' '{where}' — {e}") 
        # Логирование ошибки
        log(command, success=False, error=str(e))