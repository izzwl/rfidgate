__name__ = 'Orange Pi Zero 2'

from time import sleep
import OPi.GPIO as GPIO
from settings import DEVICE


class Controller(object):
    def __init__(self,*args, **kwargs):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(int(DEVICE['gpio_gate_pin']),GPIO.OUT)
        GPIO.setup(int(DEVICE['gpio_led_pin']),GPIO.OUT)
        # Set pin sensor/push button tutup_gate to be an input pin and set initial value to be pulled low (off)
        GPIO.setup(int(DEVICE['gpio_tutup_gate_pin']), GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
    
    def __del__(self):
        print("Cleanup GPIO")
        GPIO.cleanup()
    
    def blip_led(self):
        GPIO.output(int(DEVICE['gpio_led_pin']),GPIO.HIGH)
        sleep(1)
        GPIO.output(int(DEVICE['gpio_led_pin']),GPIO.LOW)    
    
    def buka_gate(self):
        GPIO.output(int(DEVICE['gpio_gate_pin']),GPIO.HIGH)
        self.blip_led()   
        sleep(1)
        self.tutup_gate()

    def tutup_gate(self):
        GPIO.output(int(DEVICE['gpio_gate_pin']),GPIO.LOW)    

    def listen_tutup_gate(self):
        while True: # Run forever
            if GPIO.input(int(DEVICE['gpio_tutup_gate_pin'])) == GPIO.HIGH:
                print("Tutup Gate!")
                self.tutup_gate()    
                sleep(1)

