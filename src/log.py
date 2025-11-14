from datetime import datetime

LOG_FILE = 'shell.log'

def log(command, success=True, error=None):
    timestamp = datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')
    with open(LOG_FILE, 'a') as lf:
        if success:
            lf.write(f'{timestamp} {command}\n')
        else:
            lf.write(f'{timestamp} ERROR: {error}\n')