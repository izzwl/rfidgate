__name__ = 'Raspberry PI 3B'

import RPi.GPIO as GPIO
from settings import DEVICE


class Controller(object):
    def __init__(self,*args, **kwargs):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(int(DEVICE['gpio_gate_pin']),GPIO.OUT)
        # Set pin sensor/push button tutup_gate to be an input pin and set initial value to be pulled low (off)
        GPIO.setup(DEVICE['gpio_tutup_gate_pin'], GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
    
    def buka_gate(self):
        GPIO.output(int(DEVICE['gpio_gate_pin']),GPIO.HIGH)

    def tutup_gate(self):
        GPIO.output(int(DEVICE['gpio_gate_pin']),GPIO.LOW)    

    def listen_tutup_gate(self):
        while True: # Run forever
            if GPIO.input(int(DEVICE['gpio_tutup_gate_pin'])) == GPIO.HIGH:
                print("Tutup Gate!")
                GPIO.output(int(DEVICE['gpio_gate_pin']),GPIO.LOW)    
