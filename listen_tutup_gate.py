from settings import API_URL,DEVICE

def listening():
    try:
        device_module = __import__("_"+DEVICE['type'])
        dev = device_module.Controller()
    except Exception as e:
        print(e)
        dev = None
    try:
        # dev.buka_gate()
        dev.listen_tutup_gate()
    except Exception as e:
        print(e)