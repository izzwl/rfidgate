import threading
from time import sleep
import keyboard
import requests
from logger import log
from settings import API_URL,DEVICE
from lcd_matrix import LCD
from twt import ThreadWithTrace
error_lines = {
    'line1':"+------------------+",
    'line2':"|  ERROR /  GAGAL  |",
    'line3':"|  XXXXXXXXXXXXXX  |",
    'line4':"+------------------+",
}

error_lines = {
    'line1':"+------------------+",
    'line2':"|  ERROR /  GAGAL  |",
    'line3':"|     YAUDAAAH     |",
    'line4':"+------------------+",
}
not_connected_lines = {
    'line1':"+------------------+",
    'line2':"|  DISCONNECT FROM |",
    'line3':"|     SERVER       |",
    'line4':"+------------------+",
}

def get_device(lcd):
    t_lcd_text = None
    while True:
        try:
            device_module = __import__("_"+DEVICE['type'])
            dev = device_module.Controller()
        except Exception as e:
            # print(e)
            log.error(str(e))
            dev = None
        if not dev or dev.not_connected:
            for k,v in not_connected_lines.items():
                log.error(v)
            if t_lcd_text : t_lcd_text.kill()
            t_lcd_text = ThreadWithTrace(target=lcd.print_text,kwargs={
                'durasi':5,
                **not_connected_lines
            })
            t_lcd_text.start()
            sleep(5)
            continue
        else:
            break
    return dev

def listening():
    lcd = LCD()
    t_lcd = None
    t_lcd_text = None
    t_led = None
    t_led_error = None


    lcd.t_main = ThreadWithTrace(target=lcd.main)
    lcd.t_main.start()

    
    dev = get_device(lcd)


    while True:
        dev.cek_tutup_gate()
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
                # print(endpoint)
                # log.info(endpoint)
                r = requests.get(
                    endpoint,
                    timeout=3
                )
                res_json = r.json() 
                results.update({ k:v for k,v in res_json.items()})
                
            except:
                results['error'] = 'requests error'
                if t_lcd_text:t_lcd_text.kill()
                if t_led:t_led.kill()    
                # if t_led_error:t_led_error.kill()    
                
                t_led = ThreadWithTrace(target=dev.blip_led_error)
                t_led.start()
                t_lcd_text = ThreadWithTrace(target=lcd.print_text,kwargs={
                    'durasi':dev.second_error_blip,
                    **not_connected_lines
                })
                t_lcd_text.start()
                for k,v in not_connected_lines.items():
                    log.error(v)
                continue

        
        # print(results['gate_trigger'],results)
        # log.info(results['gate_trigger'])
        log.debug(str(results))
        if str(results['gate_trigger'])=='1':
            try:
                # dev.buka_gate()
                # t_buka = threading.Thread(target=dev.buka_gate)
                # t_buka.start()
                
                if t_lcd_text : t_lcd_text.kill()
                if t_lcd : t_lcd.kill()
                if t_led : t_led.kill()
                success_lines = {
                    'line1':results['datetime'],
                    'line2':results['nik'],
                    'line3':results['name'][0:20],
                    # 'line4':'BERHASIL'.rjust(20),
                }
                
                if results['raw'][-1] == "1":
                    success_lines['line4'] = 'MASUK - BERHASIL'.rjust(20)
                elif results['raw'][-1] == "0":
                    success_lines['line4'] = 'KELUAR - BERHASIL'.rjust(20)
                
                t_led = ThreadWithTrace(target=dev.blip_led)
                t_led.start()
                t_lcd = ThreadWithTrace(target=dev.blip_led_lcd)
                t_lcd.start()
                t_lcd_text = ThreadWithTrace(target=lcd.print_text,kwargs={
                    'durasi':dev.second_gate_blip,
                    # 'line1':_dt[0][0:3]+" "+tgl_jam.rjust(16),
                    **success_lines
                })
                t_lcd_text.start()
                for k,v in success_lines.items():
                    log.info(v)
            except Exception as e:
                print(e)
                log.error(str(e))
    
        if results.get('error'):
            try:
                # dev.buka_gate()
                if t_lcd_text:t_lcd_text.kill()
                if t_led:t_led.kill()    
                # if t_led_error:t_led_error.kill()    
                
                t_led = ThreadWithTrace(target=dev.blip_led_error)
                t_led.start()
                t_lcd_text = ThreadWithTrace(target=lcd.print_text,kwargs={
                    'durasi':dev.second_error_blip,
                    **error_lines
                })
                t_lcd_text.start()
                for k,v in error_lines.items():
                    log.info(v)
            except Exception as e:
                print(e)
                log.error(str(e))
                
                
        
        
        


