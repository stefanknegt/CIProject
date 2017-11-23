import os
import time
#if __name__ == "__main__":
#    os.system('xterm -e "pwd ; cd ~ ; torcs -r ~/quickrace.xml ; echo press RETURN to close this window ; read" &') # delete the echo and the read to don't stop the process and make it run quickly
#    os.system('xterm -e "pwd  ; ./start.sh ; echo press RETURN to close this window ; read" &')

def train(i):
    if i == 0:
        os.system('xterm -e " pwd ; pwd ; torcs -r $PWD/quickraces/quickrace-forza.xml  " &') # delete the echo and the read to don't stop the process and make it run quickly
        os.system('xterm -e " pwd ; ./start.sh " &')
        return 'forza'
    elif i == 1:
        os.system('xterm -e " pwd ; pwd ; torcs -r $PWD/quickraces/quickrace-ruudskogen.xml  " &') # delete the echo and the read to don't stop the process and make it run quickly
        os.system('xterm -e " pwd ; ./start.sh " &')
        return 'ruudskogen'
    elif i == 2:
        os.system('xterm -e " pwd ; pwd ; torcs -r $PWD/quickraces/quickrace-aalborg.xml  " &') # delete the echo and the read to don't stop the process and make it run quickly
        os.system('xterm -e " pwd ; ./start.sh " &')
        return 'aalborg'
    elif i == 3:
        os.system('xterm -e " pwd ; pwd ; torcs -r $PWD/quickraces/quickrace-corkscrew.xml  " &') # delete the echo and the read to don't stop the process and make it run quickly
        os.system('xterm -e " pwd ; ./start.sh " &')
        return 'corkscrew'
