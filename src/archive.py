import zipfile   # модуль для работы с ZIP-архивами
import tarfile   # модуль для работы с TAR-архивами
from log import log   # функция логирования
import os        # модуль для работы с файловой системой

def create_zip(st):

    if len(st) < 3:
        print("Ошибка: недостаточно аргументов для создания ZIP")
        log(" ".join(st), success=False, error="Not enough arguments")
        return

    folder = st[1]        # папка для архивации
    archive_name = st[2]  # имя архива
    command = ' '.join(st)

    try:
        with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(folder):
                for file in files:
                    full_path = os.path.join(root, file)
                    arcname = os.path.relpath(full_path, folder)
                    zipf.write(full_path, arcname)
        print(f"ZIP-архив создан: {archive_name}")
        log(command, success=True)
    except Exception as e:
        print(f"Ошибка при создании ZIP: {e}")
        log(command, success=False, error=str(e))


def extract_zip(st):
    
    if len(st) < 2:
        print("Ошибка: не указан ZIP-архив для распаковки")
        log(" ".join(st), success=False, error="No archive specified")
        return

    archive_name = st[1]
    command = ' '.join(st)

    try:
        with zipfile.ZipFile(archive_name, 'r') as zipf:
            zipf.extractall()
        print(f"ZIP-архив распакован: {archive_name}")
        log(command, success=True)
    except Exception as e:
        print(f"Ошибка при распаковке ZIP: {e}")
        log(command, success=False, error=str(e))


def create_tar(st):

    if len(st) < 3:
        print("Ошибка: недостаточно аргументов для создания TAR.GZ")
        log(" ".join(st), success=False, error="Not enough arguments")
        return

    folder = st[1]
    archive_name = st[2]
    command = ' '.join(st)

    try:
        with tarfile.open(archive_name, "w:gz") as tarf:
            tarf.add(folder, os.path.basename(folder))
        print(f"TAR.GZ-архив создан: {archive_name}")
        log(command, success=True)
    except Exception as e:
        print(f"Ошибка при создании TAR.GZ: {e}")
        log(command, success=False, error=str(e))


def extract_tar(st):

    if len(st) < 2:
        print("Ошибка: не указан TAR.GZ-архив для распаковки")
        log(" ".join(st), success=False, error="No archive specified")
        return

    archive_name = st[1]
    command = ' '.join(st)

    try:
        with tarfile.open(archive_name, "r:gz") as tarf:
            tarf.extractall()
        print(f"TAR.GZ-архив распакован: {archive_name}")
        log(command, success=True)
    except Exception as e:
        print(f"Ошибка при распаковке TAR.GZ: {e}")
        log(command, success=False, error=str(e))

