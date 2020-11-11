import serial
import RPi.GPIO as gpio
import Adafruit_DHT as dht
import time
import sys
import warnings.filterwarnings('ignore')

port = '/dev/ttyACM0'
brate = 115200
cmd = 'temp'

DAT = 11

gpio.cleanup()
gpio.setmode(gpio.BCM)

ser = serial.Serial(port, baudrate= brate, timeout = None)


try:
      while True:
            humidity, temperature = dht.read_retry(dht.DHT22, DAT)
            humid = round(humidity, 1)
            temp = round(temperature, 1)
            print("Temp=%d\tHumid=%d" % (temp, humid))

            #Raspberry Pi 에서 Arduino 로 보낼 Temp 값 전송 코드
            #써야함.
            #tp = input(temp)
            #ser.write(tp.encode())
            #?


            #Serial 통신, 받는 코드
            if ser.in_waiting != 0:
                content = seri.readline()
                #print(content)
                print(content[:-2].decode())
                time.sleep(2)

except KeyboardInterrupt:
     gpio.cleanup()
     sys.exit()
