import RPi.GPIO as gpio
import time
import warnings
import sys
warnings.filterwarnings('ignore')

FLOW = 24

gpio.setmode(gpio.BCM)
gpio.setup(FLOW, gpio.IN)

try:
    while True:
        if gpio.input(FLOW) == gpio.HIGH:
            print('1')
        else:
            print('0')
        time.sleep(2)

except KeyboardInterrupt:
    gpio.cleanup()
    sys.exit()
