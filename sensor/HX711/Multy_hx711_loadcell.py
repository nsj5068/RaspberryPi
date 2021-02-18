import time
import sys
import warnings
import pymysql
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

hx1 = HX711(24, 22)  #DT, SCK
hx2 = HX711(25, 23)
#hx3 = HX711(27, 17)

#------------hx1

hx1.set_reading_format('MSB', 'MSB')
hx1.set_reference_unit(4.2645)  # setting 1g
#hx.set_reference_unit(referenceUnit)   # setting 1g

hx1.reset()
hx1.tare()

#------------hx2

hx2.set_reading_format('MSB', 'MSB')
hx2.set_reference_unit(4.2645)  # setting 1g
#hx.set_reference_unit(referenceUnit)   # setting 1g

hx2.reset()
hx2.tare()

#------------hx3

#hx3.set_reading_format('MSB', 'MSB')
#hx3.set_reference_unit(4.2645)  # setting 1g
#hx.set_reference_unit(referenceUnit)   # setting 1g

#hx3.reset()
#hx3.tare()

print('Tare done! Add weight now...')

while True:
    try:
         val1 = hx1.get_weight(5)
         val2 = hx2.get_weight(5)
         #val3 = hx3.get_weight(5)
         w1 = val1//93
         w2 = val2//93
         #w3 = val3//93

         print('val1=%15.2f  w1=%5dg' % (val1, w1))
         print('val2=%15.2f  w2=%5dg\n' % (val2, w2))
         #print('val3=%15.2f  w3=%5dg\n' % (val3, w3))

         hx1.power_down()
         hx2.power_down()
         #hx3.power_down()

         hx1.power_up()
         hx2.power_up()
         #hx3.power_up()

         #insertDB(w1, w2, w3)
         time.sleep(60)

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
