from datetime import datetime

# Файл для записи логов
LOG_FILE = 'shell.log'

def log(command, success=True, error=None):
    
    # Получаем текущую дату и время в заданном формате
    timestamp = datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')
    
    # Открываем файл логов в режиме добавления
    with open(LOG_FILE, 'a') as lf:
        if success:
            # Логируем успешное выполнение команды
            lf.write(f'{timestamp} {command}\n')
        else:
            # Логируем ошибку с сообщением
            lf.write(f'{timestamp} ERROR: {error}\n')