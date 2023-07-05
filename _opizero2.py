__name__ = 'Orange Pi Zero 2'

from time import sleep
import requests
from logger import log
import OPi.GPIO as GPIO
from settings import DEVICE,IS_REMOTE_CONFIG,API_URL,STATIC_TEXT
from lcd_matrix import LCD

class Controller(object):
    second_blip = 0.3
    second_error_blip = 0.3
    pin_pwm = 7
    device = None
    not_connected = False
    def __init__(self,device=DEVICE,*args, **kwargs):
        self.device=device
        if IS_REMOTE_CONFIG:
            endpoint = API_URL+'get_device_config'
            # print('initial--get config from web')
            log.info('initial--get config from web')
            # print(endpoint)
            log.info(endpoint)
            try:
                r = requests.get(
                    endpoint,
                    timeout=30
                )
                res_json = r.json()
                self.device={
                    **self.device,
                    **res_json['device']
                }
            except:
                self.not_connected = True
            # print(self.device)
            if not self.not_connected:
                log.info("+{}+".format("".rjust(40,"-")))
                for k,v in self.device.items():
                    log.info("|{}|".format(f"{str(k)} : {str(v)}".ljust(40)))
                log.info("+{}+".format("".rjust(40,"-")))

        if self.device.get('gpio_power_pin'):
            self.pin_pwm = int(self.device['gpio_power_pin'])
        if self.device.get('gpio_led_pin_sleep'):
            self.second_blip = round(float(self.device['gpio_led_pin_sleep']),2)
        if self.device.get('gpio_gate_pin_sleep'):
            self.second_gate_blip = round(float(self.device['gpio_gate_pin_sleep']),2)
        if self.device.get('gpio_error_led_pin_sleep'):
            self.second_error_blip = round(float(self.device['gpio_error_led_pin_sleep']),2)
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(int(self.pin_pwm),GPIO.OUT)
        GPIO.output(int(self.pin_pwm),GPIO.HIGH)

        GPIO.setup(int(self.device['gpio_led_pin']),GPIO.OUT)
        GPIO.setup(int(self.device['gpio_error_led_pin']),GPIO.OUT)
        if self.device['gpio_gate_pin']:
            GPIO.setup(int(self.device['gpio_gate_pin']),GPIO.OUT)
        # Set pin sensor/push button tutup_gate to be an input pin and set initial value to be pulled low (off)
        if self.device['gpio_tutup_gate_pin']:
            GPIO.setup(int(self.device['gpio_tutup_gate_pin']), GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
        # self.blip_led(3)
        self.blip_pwm(3)

    def __del__(self):
        # print("Cleanup GPIO")
        log.info("Cleanup GPIO")
        GPIO.cleanup()
    
    def blip_pwm(self,sec=5):
        while True:
            if sec > 0:
                GPIO.output(int(self.pin_pwm),GPIO.HIGH)
                sleep(0.5)
                GPIO.output(int(self.pin_pwm),GPIO.LOW)
                sleep(0.5)
                sec -= 1
            else:
                break
        GPIO.output(int(self.pin_pwm),GPIO.HIGH)
        

    def low_all_led(self):
        GPIO.output(int(self.device['gpio_led_pin']),GPIO.LOW)    
        GPIO.output(int(self.device['gpio_gate_pin']),GPIO.LOW)
        GPIO.output(int(self.device['gpio_error_led_pin']),GPIO.LOW)

    def blip_led(self,second=0):
        self.low_all_led()
        GPIO.output(int(self.device['gpio_led_pin']),GPIO.HIGH)
        GPIO.output(int(self.pin_pwm),GPIO.LOW)
        sleep(round(float(second),2) if second else self.second_blip)
        GPIO.output(int(self.device['gpio_led_pin']),GPIO.LOW)    
        GPIO.output(int(self.pin_pwm),GPIO.HIGH)

    def blip_led_lcd(self):
        self.low_all_led()
        GPIO.output(int(self.device['gpio_gate_pin']),GPIO.HIGH)
        sleep(self.second_gate_blip)
        GPIO.output(int(self.device['gpio_gate_pin']),GPIO.LOW)

    def blip_led_error(self):
        self.low_all_led()
        GPIO.output(int(self.device['gpio_error_led_pin']),GPIO.HIGH)
        GPIO.output(int(self.pin_pwm),GPIO.LOW)
        sleep(self.second_error_blip)
        GPIO.output(int(self.device['gpio_error_led_pin']),GPIO.LOW)
        GPIO.output(int(self.pin_pwm),GPIO.HIGH)
    
    def buka_gate(self):
        if self.device['gpio_gate_pin']:
            GPIO.output(int(self.device['gpio_gate_pin']),GPIO.HIGH)
            self.blip_led()   
            sleep(int(self.device['gpio_gate_pin_sleep'])-self.second_blip)
            self.tutup_gate()
        pass

    def tutup_gate(self):
        if self.device['gpio_gate_pin']:
            GPIO.output(int(self.device['gpio_gate_pin']),GPIO.LOW)    
        pass

    def _listen_tutup_gate(self):
        while True: # Run forever
            if GPIO.input(int(self.device['gpio_tutup_gate_pin'])) == GPIO.HIGH:
                print("Tutup Gate!")
                log.info("Tutup Gate!")
                self.tutup_gate()    
                sleep(1)
    
    def cek_tutup_gate(self):
        if self.device['gpio_tutup_gate_pin']:
            if GPIO.input(int(self.device['gpio_tutup_gate_pin'])) == GPIO.HIGH:
                self.tutup_gate()    
                print("Tutup Gate!")
                log.info("Tutup Gate!")
                sleep(1)
        pass

