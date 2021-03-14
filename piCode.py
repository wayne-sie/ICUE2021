from time import sleep
import sys
from mfrc522 import SimpleMFRC522
import RPi.GPIO as gpio

import requests

reader = SimpleMFRC522()

try:
    while True:
        print("Hold a tag near the reader")
        id, text = reader.read()
        print("ID: %s\nText: %s" % (id,text))
        URL = f'http://192.168.0.18:5000'
        params = {
            'rfid': id,
            'num': text,
        }
        r = requests.get(url = URL, params)

        data = r.json()

        # print(data)
        
        sleep(5)
        
except KeyboardInterrupt:
    gpio.cleanup()
    raise