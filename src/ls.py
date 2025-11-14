import os
import stat
import time
from log import log


def ls(st):
    
    long_f = '' # переменная для хранения флага
    path = '.'    # путь по умолчанию — текущая директория

    # разбор токенов, начиная со второго (первый всегда "ls")
    if len(st) > 1:
        for t in st[1:]:
            if t ==  '-l': # если токен "-l", считаем его флагом
                long_f = t
            else:
                path = t

    command = ' '.join(st) # собираем команду обратно в строку для логирования
    try:
        entries = os.listdir(path) # получаем список файлов и папок в директории
        for entry in entries:
            full_path = os.path.join(path, entry) # формируем полный путь
            
            if long_f == '-l':  # если указан флаг "-l", выводим подробную информацию
                stats = os.stat(full_path)   # получаем статистику файла
                permissions = stat.filemode(stats.st_mode)  # права доступа
                size = stats.st_size  # размер файла в байтах
                mtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stats.st_mtime)) # время последнего изменения в читаемом формате
                print(f'{permissions} {size:>10} {mtime} {entry}')
            else:
                print(entry)  # если флаг не указан, выводим только имя файла
        log(command, success=True)
    except Exception as e:
        print(f"Ошибка: не удалось отобразить '{path}' — {e}")
        log(command, success=False, error=str(e))
