import os
import time
#if __name__ == "__main__":
#    os.system('xterm -e "pwd ; cd ~ ; torcs -r ~/quickrace.xml ; echo press RETURN to close this window ; read" &') # delete the echo and the read to don't stop the process and make it run quickly
#    os.system('xterm -e "pwd  ; ./start.sh ; echo press RETURN to close this window ; read" &')

training = True

while training:
    if __name__ == "__main__":
        term1 = os.system('xterm -e "pwd ; cd ~ ; torcs -r ~/quickrace.xml  " &') # delete the echo and the read to don't stop the process and make it run quickly
        term2 = os.system('xterm -e "pwd  ; ./start.sh " &')
        time.sleep(25)

