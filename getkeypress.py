import keyboard
import requests
from settings import API_URL
while True:
    texts = list(keyboard.get_typed_strings(keyboard.record(until='enter')))
    data = ''
    try:
        if texts[0] != '':
            print(texts[0])
            data = texts[0]
    except:
        continue 

    #eksekusi request ke api untuk cek nik dan record data
    if data:
        r = requests.get(API_URL+'cek_user/%s'%(data))
        print(r.json())


