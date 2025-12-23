import os
import stat
import time
from log import log


def ls(st: list) -> None:
    """
    Функция для отображения содержимого директории
    
    Параметры:
    st - список аргументов команды (первый элемент - 'ls')
    """
    
    long_f = ''   # Флаг подробного вывода (-l)
    path = '.'    # Путь к директории (по умолчанию текущая)
    
    # Обработка аргументов команды
    if len(st) > 1:
        # Проверяем наличие флага подробного вывода
        if st[1] == '-l':
            long_f = st[1]  # Устанавливаем флаг подробного вывода
        else:
            path = st[1]    # Устанавливаем указанный путь
    
    command = ' '.join(st)  # Полная команда для логирования
    
    try:
        # Получаем список файлов и папок в указанной директории
        entries = os.listdir(path)
        
        # Обрабатываем каждый элемент в директории
        for entry in entries:
            full_path = os.path.join(path, entry)  # Полный путь к элементу
            
            if long_f == '-l':
                # Подробный вывод с дополнительной информацией
                stats = os.stat(full_path)  # Получаем статистику файла
                permissions = stat.filemode(stats.st_mode)  # Права доступа
                size = stats.st_size  # Размер файла
                # Время последнего изменения
                mtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stats.st_mtime))
                # Форматированный вывод с выравниванием
                print(f'{permissions} {size:>10} {mtime} {entry}')
            else:
                # Простой вывод только имен файлов
                print(entry) 
                
        # Логирование успешного выполнения
        log(command, success=True)
        
    except Exception as e:
        # Обработка ошибок при чтении директории
        print(f"Ошибка: не удалось отобразить '{path}' — {e}")
        log(command, success=False, error=str(e))