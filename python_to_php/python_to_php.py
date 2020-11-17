#DHT 22 를 이용함.
#워드프레스 환경, phpmyadmin.


import urllib
import urllib.request
import http.client as httplib
import RPi.GPIO as gpio
import time
import Adafruit_DHT as dht
import sys
import warnings
warnings.filterwarnings('ignore')

DAT = 11

gpio.cleanup()
gpio.setmode(gpio.BCM)


def insertWebdb(temp, humid):
        headers = {"Content-type":"application/x-www-form-urlencoded"}
        params = urllib.parse.urlencode({'temp_1':temp, 'humid_1':humid}) #데이터 들어갈 애들

        conn=httplib.HTTPConnection("*******.*****.net:80")   #"host:port number"

        conn.request("POST", "/jeju/exam/nsj_test.php", params, headers)

        response = conn.getresponse()
        data = response.read()
        print (data)

        conn.close()

        #최선책

def urllibWebdb(temp, humid):
        params = urllib.parse.urlencode({'temp_1':temp, 'humid_1':humid})

        binary_data = params.encode('utf-8')

        resp = urllib.request.urlopen('http://*******.*****.net/*****/*******/test.php', binary_data)


        #차선책

try:
       while True:
             humidity, temperature = dht.read_retry(dht.DHT22, DAT)
             humid = round(humidity, 1)
             temp = round(temperature, 1)
             print("Temp=%d\tHumid=%d" % (temp, humid))
             insertWebdb(temp,humid)
             #urllibWebdb(temp,humid)

             time.sleep(5)

except KeyboardInterrupt:
     gpio.cleanup()
     sys.exit()
