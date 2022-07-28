import threading
from time import sleep
from settings import API_URL,DEVICE
import listen_keypress
import listen_tutup_gate

if __name__ == '__main__':
    t_keypress = threading.Thread(target=listen_keypress.listening)
    # t_keypress.daemon = True
    t_keypress.start()
    t_tutup_gate = threading.Thread(target=listen_tutup_gate.listening)
    # t_tutup_gate.daemon = True
    t_tutup_gate.start()

