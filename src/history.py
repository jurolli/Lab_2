from datetime import datetime

history_file = ".history"

def hist_history(h, st):
    """
    Записывает команду с её номером h в файл истории.
    """
    h +=1
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    command = " ".join(st)
    with open(history_file, "a", encoding="utf-8") as hf:
        hf.write(f"{timestamp} [{h}.] {command}\n")



def show_history(st):
    """
    Выводит последние n команд из истории.
    st — токенизированный массив, где st[0] = 'show_history', st[1] = n.
    """
    try:
        n = int(st[1])  # параметр n берём из массива
        with open(history_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for i, line in enumerate(lines[-n:], start=1):
            print(f"{i}. {line.strip()}")
    except (FileNotFoundError, ValueError, IndexError):
        print("История пуста или параметр n некорректен")
