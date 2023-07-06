#!/usr/bin/python

import smbus
import time
from settings import STATIC_TEXT
from twt import ThreadWithTrace
class LCD(object):
  # Define some device parameters
  I2C_ADDR  = 0x27 # I2C device address
#  I2C_ADDR  = 0x3F # I2C device address
  LCD_WIDTH = 20   # Maximum characters per line

  # Define some device constants
  LCD_CHR = 1 # Mode - Sending data
  LCD_CMD = 0 # Mode - Sending command

  LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
  LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
  LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
  LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line

  LCD_BACKLIGHT  = 0x08  # On
  #LCD_BACKLIGHT = 0x00  # Off

  ENABLE = 0b00000100 # Enable bit

  # Timing constants
  E_PULSE = 0.0005
  E_DELAY = 0.0005

  #Open I2C interface
  bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
  #bus = smbus.SMBus(1) # Rev 2 Pi uses 1
  push_text = False
  
  def lcd_init(self):
    # Initialise display
    self.lcd_byte(0x33,self.LCD_CMD) # 110011 Initialise
    self.lcd_byte(0x32,self.LCD_CMD) # 110010 Initialise
    self.lcd_byte(0x06,self.LCD_CMD) # 000110 Cursor move direction
    self.lcd_byte(0x0C,self.LCD_CMD) # 001100 Display On,Cursor Off, Blink Off 
    self.lcd_byte(0x28,self.LCD_CMD) # 101000 Data length, number of lines, font size
    self.lcd_byte(0x01,self.LCD_CMD) # 000001 Clear display
    time.sleep(self.E_DELAY)

  def lcd_byte(self, bits, mode):
    # Send byte to data pins
    # bits = the data
    # mode = 1 for data
    #        0 for command

    bits_high = mode | (bits & 0xF0) | self.LCD_BACKLIGHT
    bits_low = mode | ((bits<<4) & 0xF0) | self.LCD_BACKLIGHT

    # High bits
    self.bus.write_byte(self.I2C_ADDR, bits_high)
    self.lcd_toggle_enable(bits_high)

    # Low bits
    self.bus.write_byte(self.I2C_ADDR, bits_low)
    self.lcd_toggle_enable(bits_low)

  def lcd_toggle_enable(self,bits):
    # Toggle enable
    time.sleep(self.E_DELAY)
    self.bus.write_byte(self.I2C_ADDR, (bits | self.ENABLE))
    time.sleep(self.E_PULSE)
    self.bus.write_byte(self.I2C_ADDR,(bits & ~self.ENABLE))
    time.sleep(self.E_DELAY)

  def lcd_string(self,message,line):
    # Send string to display

    message = message.ljust(self.LCD_WIDTH," ")

    self.lcd_byte(line, self.LCD_CMD)

    for i in range(self.LCD_WIDTH):
      self.lcd_byte(ord(message[i]),self.LCD_CHR)

  def print_text(self,durasi=2,line1="",line2="",line3="",line4="",):
    # Main program block

    # Initialise display
    if self.t_main:
      self.t_main.kill()
    
    self.lcd_init()
    # print_string 
    self.lcd_string(f"{line1}",self.LCD_LINE_1)
    self.lcd_string(f"{line2}",self.LCD_LINE_2)
    self.lcd_string(f"{line3}",self.LCD_LINE_3)
    self.lcd_string(f"{line4}",self.LCD_LINE_4)
    time.sleep(int(durasi))
    # self.lcd_byte(0x01, self.LCD_CMD)
    # self.push_text = False
    # self.main()

    self.t_main = ThreadWithTrace(target=self.main)
    self.t_main.start()

  def main(self,line1="",line2="",line3="",line4=""):
    # Main program block

    # Initialise display

    self.lcd_init()
    tiktok = False
    while True:
      tiktok = not tiktok
      cursor = " ||" if tiktok else " |"
      if line1:
        ln = line1 
      else:
        ln = time.strftime('%Y-%m-%d  %H:%M') + cursor
      self.lcd_string(f"{ln}",self.LCD_LINE_1)
      # self.lcd_string(f"{line2}" if line2 else "                    ",self.LCD_LINE_2)
      # self.lcd_string(f"{line3}" if line3 else "                    ",self.LCD_LINE_3)
      # self.lcd_string(f"{line4}" if line4 else "<<<<< Gate IN <<<<< ",self.LCD_LINE_4)
      # self.lcd_string(f"{line1}" if line1 else STATIC_TEXT[1],self.LCD_LINE_1)
      self.lcd_string(f"{line2}" if line2 else STATIC_TEXT[2],self.LCD_LINE_2)
      self.lcd_string(f"{line3}" if line3 else STATIC_TEXT[3],self.LCD_LINE_3)
      self.lcd_string(f"{line4}" if line4 else STATIC_TEXT[4],self.LCD_LINE_4)
      time.sleep(1)
      
      # else:
      #   break

  def run_main(self,line1="",line2="",line3="",line4=""):
    try:
      self.main(line1,line2,line3,line4)
    except KeyboardInterrupt:
      pass
    finally:
      self.lcd_byte(0x01, self.LCD_CMD)

