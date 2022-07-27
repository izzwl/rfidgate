__name__ = 'Raspberry PI 3B'

import RPi.GPIO as GPIO
from settings import DEVICE


class Controller(object):
    def __init__(self):
        GPIO.setup(GPIO.BOARD)
        GPIO.setup(24,GPIO.OUT)
    
    def buka_gate(self):
        GPIO.output(24,GPIO.HIGH)

    def tutup_gate(self):
        GPIO.output(24,GPIO.LOW)    
