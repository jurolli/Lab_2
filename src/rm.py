import shutil   # модуль для удаления директорий рекурсивно
import os       # модуль для работы с файловой системой
from log import log   # функция логирования

TRASH_DIR = ".trash"    # каталог для временного хранения удалённых объектов

# создаём каталог .trash, если он ещё не существует
os.makedirs(TRASH_DIR, exist_ok=True)

def rm(st):

    recur = ''   # флаг для рекурсивного удаления
    path = ''    # путь к файлу или каталогу

    # разбор токенов
    if len(st) < 2:
        print("Ошибка: не указан путь для удаления")
        log(" ".join(st), success=False, error="No path specified")
        return

    if st[1] == '-r':   # если указан флаг -r
        recur = '-r'
        if len(st) < 3:
            print("Ошибка: не указан каталог для рекурсивного удаления")
            log(" ".join(st), success=False, error="No directory specified for recursive delete")
            return
        path = st[2]
    else:
        path = st[1]

    command = ' '.join(st)   # собираем команду обратно в строку для логирования

    # защита от удаления корня или родительского каталога
    if path in ['/', '..']:
        error = 'Удаление запрещено: корневой или родительский каталог'
        print(f'Ошибка: {error}')
        log(command, success=False, error=error)
        return

    try:
        # проверяем, существует ли путь
        if not os.path.exists(path):
            raise FileNotFoundError('Файл или каталог не существует')

        # если путь — каталог
        if os.path.isdir(path):
            if recur == '':   # без флага -r удалять каталог нельзя
                raise IsADirectoryError('Это каталог. Используйте -r для рекурсивного удаления')
            elif recur == '-r':   # рекурсивное удаление каталога
                confirm = input(f"Вы уверены, что хотите удалить каталог '{path}' и всё его содержимое? (y/n): ")
                if confirm.lower() != 'y':   # если пользователь отказался
                    print('Удаление отменено.')
                    log(command, success=False, error='Удаление отменено пользователем')
                    return
                # перемещаем каталог в .trash
                trash_path = os.path.join(TRASH_DIR, os.path.basename(path))
                # если файл с таким именем уже есть в .trash, добавляем уникальный суффикс
                if os.path.exists(trash_path):
                    import time
                    trash_path = os.path.join(TRASH_DIR, f"{os.path.basename(path)}_{int(time.time())}")
                shutil.move(path, trash_path)
        else:
            # перемещаем файл в .trash вместо прямого удаления
            trash_path = os.path.join(TRASH_DIR, os.path.basename(path))
            # если файл с таким именем уже есть в .trash, добавляем уникальный суффикс
            if os.path.exists(trash_path):
                import time
                trash_path = os.path.join(TRASH_DIR, f"{os.path.basename(path)}_{int(time.time())}")
            shutil.move(path, trash_path)

        print(f'Удалено: {path}')   # сообщение об успехе
        log(command, success=True)   # логируем успешное выполнение

    except Exception as e:   # если возникла ошибка
        print(f"Ошибка: не удалось удалить '{path}' — {e}")   # выводим сообщение об ошибке
        log(command, success=False, error=str(e))   # логируем неудачное выполнение
