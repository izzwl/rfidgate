__name__ = 'Raspberry PI 3B'

import RPi.GPIO as GPIO
from settings import DEVICE


class Controller(object):
    def __init__(self,*args, **kwargs):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(DEVICE['gpio_gate_pin'],GPIO.OUT)
    
    def buka_gate(self):
        GPIO.output(DEVICE['gpio_gate_pin'],GPIO.HIGH)

    def tutup_gate(self):
        GPIO.output(DEVICE['gpio_gate_pin'],GPIO.LOW)    
