from time import sleep
from unittest import result
import keyboard
import requests
from settings import API_URL,DEVICE
while True:
    #listen keypress
    texts = list(keyboard.get_typed_strings(keyboard.record(until='enter')))
    data = ''
    res_json = None

    results = {
        'rfid':'',
        'gate_trigger':0,
    }

    try:
        if texts[0] != '':
            results['rfid'] = texts[0]
            data = texts[0]
    except:
        results['error'] = 'keypress listen error'

    #eksekusi request ke api untuk cek rfid dan record data
    if data:
        try:
            endpoint = API_URL+'cek_user/%s/%s'%(data,DEVICE['role'])
            print(endpoint)
            r = requests.get(
                endpoint,
                timeout=3
            )
            res_json = r.json() 
            results.update({ k:v for k,v in res_json.items()})
            
        except:
            results['error'] = 'requests error'

    
    print(results['gate_trigger'],results)

    if results['gate_trigger']=='1':
        # device_module = getattr(__import__('.',fromlist=[DEVICE['type']]),DEVICE['type'])
        try:
            device_module = __import__("_"+DEVICE['type'])
            dev = device_module.Controller()
            dev.buka_gate()
        except Exception as e:
            print(e)

        
        
        


