import RPi.GPIO as gpio
import time
import sys
import warnings
warnings.filterwarnings('ignore')

gpio.cleanup()

LED1 = 26
LED2 = 16
LED3 = 20
LED4 = 21

gpio.setmode(gpio.BCM)
gpio.setup(LED1, gpio.OUT)
gpio.setup(LED2, gpio.OUT)
gpio.setup(LED3, gpio.OUT)
gpio.setup(LED4, gpio.OUT)


while True:
           gpio.output(LED4, gpio.LOW)
           gpio.output(LED1, gpio.HIGH)
           print('LED4 OFF, LED1 ON')
           time.sleep(1)
           gpio.output(LED1, gpio.LOW)
           gpio.output(LED2, gpio.HIGH)
           print('LED1 OFF, LED2 ON')
           time.sleep(1)
           gpio.output(LED2, gpio.LOW)
           gpio.output(LED3, gpio.HIGH)
           print('LED2 OFF, LED3 ON')
           time.sleep(1)
           gpio.output(LED3, gpio.LOW)
           gpio.output(LED4, gpio.HIGH)
           print('LED3 OFF, LED4 ON')
           time.sleep(1)
