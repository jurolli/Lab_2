import os
import shutil

# Импорт функций команд из соответствующих модулей
from ls import ls
from cp import cp
from mv import mv
from rm import rm
from cd import cd
from cat import cat

from tokenization import tokenization  # Импорт функции для разбиения команды на токены


# Инициализация файла истории команд
with open('.history', 'w', encoding='utf-8') as f:
    pass  # Создаем/очищаем файл истории

# Инициализация корзины для удаленных файлов
shutil.rmtree('.trash', ignore_errors=True)  # Удаляем старую корзину, если существует
os.mkdir('.trash')  # Создаем новую директорию для корзины


def main():
    """
    Основная функция интерпретатора командной строки.
    Реализует бесконечный цикл ввода команд и их обработку.
    """
    while True:
        # Выводим приглашение с текущей рабочей директорией
        st = input(os.getcwd() + ' ')
        
        # Разбиваем введенную строку на токены (команда + аргументы)
        st = tokenization(st)
        
        try:
            # Обработка команд в зависимости от первого токена
            if st[0] == 'ls':
                ls(st)
            elif st[0] == 'cd':
                cd(st)
            elif st[0] == 'cat':
                cat(st)
            elif st[0] == 'cp':
                cp(st)
            elif st[0] == 'mv':
                mv(st)
            elif st[0] == 'rm':
                rm(st)
            else:
                # Если команда не распознана
                print('command not found')            
                
        # Обработка различных типов исключений
        except FileNotFoundError:
            print('no such file')
        except PermissionError:
            print('no permission to read the file')
        except UnicodeError:
            print('failed to decode the file')
        except ValueError:
            print('unrecognized option')
        except Exception:
            # Общий обработчик для всех остальных исключений
            print('unrecognized option')


if __name__ == "__main__":
    # Точка входа в программу
    main()