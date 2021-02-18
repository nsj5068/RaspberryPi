import time
import sys
import warnings
warnings.filterwarnings('ignore')

EMULATE_HX711=False

referenceUnit = 1

if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711

def cleanAndExit():
    print('Cleaning...')

    if not EMULATE_HX711:
        GPIO.cleanup()

    print('Bys!')
    sys.exit()

hx = HX711(24, 22)  #DT, SCK

hx.set_reading_format('MSB', 'MSB')
hx.set_reference_unit(4.2645)  # setting 1g
#hx.set_reference_unit(referenceUnit)   # setting 1g

hx.reset()
hx.tare()

print('Tare done! Add weight now...')

while True:
    try:
         val = hx.get_weight(5)
         weight = val//93

         print('val=%15.2f  weight=%5dg' % (val, val//93))

         hx.power_down()
         hx.power_up()
         time.sleep(1)

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
