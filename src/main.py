import os
import shutil

from ls import ls
from cp import cp
from mv import mv
from rm import rm
from cd import cd
from cat import cat
from archive import *
from history import *
from grep import grep
from undo import *
from tokenization import tokenization


with open('.history', 'w', encoding='utf-8') as f:
    pass
shutil.rmtree('.trash')
os.mkdir('.trash')

h = 0
def main():
    while True:
        st = input(os.getcwd() + ' ')
        st = tokenization(st)
        try:
            if st[0] == 'ls':
                ls(st)
                hist_history(h, st)
            elif st[0] == 'cd':
                cd(st)
                hist_history(h, st)
            elif st[0] == 'cat':
                cat(st)
                hist_history(h, st)
            elif st[0] == 'cp':
                cp(st)
                hist_history(h, st)
                log_undo(st)
            elif st[0] == 'mv':
                mv(st)
                hist_history(h, st)
                log_undo(st)
            elif st[0] == 'rm':
                rm(st)
                hist_history(h, st)
                log_undo(st)
            elif st[0] == 'zip':
                create_zip(st)
                hist_history(h, st)
            elif st[0] == 'unzip':
                extract_zip(st)
                hist_history(h, st)
            elif st[0] == 'tar':
                create_tar(st)
                hist_history(h, st)
            elif st[0] == 'untar':
                extract_tar(st)
                hist_history(h, st)
            elif st[0] == 'history' and len(st) <= 2:
                show_history(st)
            elif st[0] == 'grep':
                grep(st)
                hist_history(h, st)
            elif st[0] == 'undo':
                undo()
                hist_history(h, st)
            else:
                print('command not found')
                
                    
        except FileNotFoundError:
            print('no such file')
        except PermissionError:
            print('no permission to read the file')
        except UnicodeError:
                print('failed to decode the file')
        except ValueError:
                print('unrecognized option')







if __name__ == "__main__":
    main()
