from unittest import result
import keyboard
import requests
import json
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
            results = {
                **results,
                **res_json
            }
            
        except:
            results['error'] = 'requests error'

    
    print(results['gate_trigger'],results)

    if results['gate_trigger']=='1':
        # device_module = getattr(__import__('.',fromlist=[DEVICE['type']]),DEVICE['type'])
        device_module = __import__("_"+DEVICE['type'])
        print('module_loaded',device_module.__name__)
        dev = device_module.Controller()
        dev.buka_gate()
        


