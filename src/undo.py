import os
import shutil
from datetime import datetime

UNDO_LOG = ".history"   # файл, где хранится история операций
TRASH_DIR = ".trash"    # каталог для временного хранения удалённых объектов

# создаём каталог .trash, если он ещё не существует
os.makedirs(TRASH_DIR, exist_ok=True)

def log_undo(st):
    """
    Записывает операцию в лог для возможности её отмены.
    st — токенизированный массив: [action, what, where?]
    """
    action = st[0]
    what = st[1]
    where = st[2] if len(st) > 2 else None

    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(UNDO_LOG, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} {action} {what} {where if where else ''}\n")


def undo():
    """
    Отменяет последнюю операцию из лога.
    Поддерживаются действия: cp, mv, rm.
    """
    try:
        # читаем все строки из лога
        with open(UNDO_LOG, "r", encoding="utf-8") as f:
            lines = f.readlines()

        if not lines:   # если лог пуст
            print("Нет операций для отмены")
            return

        # берём последнюю запись
        last = lines[-1].strip()
        parts = last.split()

        # разбор записи: [timestamp] action what where
        # timestamp занимает 2 части: "[2024-01-01" и "12:00:00]"
        # поэтому action начинается с parts[2]
        if len(parts) < 3:
            print("Лог операций пуст")
            return
            
        action = parts[2] 
        what = parts[3] if len(parts) > 3 else None 
        where = parts[4] if len(parts) > 4 else None

        if action == "cp":
            # отмена копирования: удаляем скопированный объект
            if where and os.path.isdir(where):
                shutil.rmtree(where)
                print(f"Отмена cp: удалён каталог {where}")
            elif where and os.path.isfile(where):
                os.remove(where)
                print(f"Отмена cp: удалён файл {where}")
            else:
                print("Ошибка: объект для удаления не найден")

        elif action == "mv":
            # отмена перемещения: возвращаем объект на место
            if where and os.path.exists(where):
                shutil.move(where, what)
                print(f"Отмена mv: {where} → {what}")
            else:
                print("Ошибка: объект для возврата не найден")

        elif action == "rm":
            # отмена удаления: восстанавливаем из .trash
            trash_path = os.path.join(TRASH_DIR, os.path.basename(what))
            if os.path.exists(trash_path):
                shutil.move(trash_path, what)
                print(f"Отмена rm: восстановлен {what}")
            else:
                print("Ошибка: объект не найден в .trash")

        # перезаписываем лог без последней строки
        with open(UNDO_LOG, "w", encoding="utf-8") as f:
            f.writelines(lines[:-1])

    except FileNotFoundError:
        print("Лог операций пуст")
    except Exception as e:
        print(f"Ошибка при отмене: {e}")
