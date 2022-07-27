from settings import API_URL,DEVICE
device_module = __import__("_"+DEVICE['type'])
print('module_loaded',device_module.__name__)

dev = device_module.Controller()
dev.listen_tutup_gate()