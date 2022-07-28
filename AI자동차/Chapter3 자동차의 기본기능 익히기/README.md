# Chapter 3 --- 자동차의 기본기능 익히기

## 3-1. LED로 전조등 구현해보기

자동차 키트의 Light는 각각 앞왼쪽(LED1:GPIO26), 앞오른쪽(LED2:GPIO16), 뒷왼쪽(LED3:GPIO20), 뒷오른쪽(LED4:GPIO21) 이다.

> 여담으로 전력문제가 가끔씩 문제가 되는 데 전력문제를 쉽게 체크하기 위해 다음 코드를 쓰면 쉽게 알 수 있다.            
> <code>cat /sys/devices/platform/leds/leds/led1/brightness</code>        
> 255면 전력 충분, 0이거나 그 아래라면 전력이 부족하다는 소리이다.

<pre>
<code>
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
</code>
</pre>


##

##
