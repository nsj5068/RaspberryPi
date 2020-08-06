# LED 제어

### 1. 개발환경
1. CNDI사의 라즈베리파이 모듈 사용
2. Octopus 5mm LED Brick - RED

### 2. 라즈베리파이와 연결
1. S : GPIO 04
2. V : VCC 5V
3. G : GND

### 3. 소스(led.py)
1. 2초 간격으로 LED가 켜졌다가 꺼짐을 반복

<pre><code>
import RPi.GPIO as gpio
import time
import sys
import warnings
warnings.filterwarnings('ignore')

LED = 4

gpio.setmode(gpio.BCM)
gpio.setup(LED, gpio.out)

try:
    while True:
        gpio.output(LED, gpio.HIGH) # gpio.HIGH = True
        time.sleep(2)
        gpio.output(LED, gpio.LOW)  # gpio.LOW = False
        time.sleep(2)
except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be executed
    gpio.cleanuo()  # Release resource
    sys.exit()
</code></pre>
