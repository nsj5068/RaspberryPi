# Chapter 3 --- 자동차의 기본기능 익히기

## 3-1. LED로 전조등 구현해보기

자동차 키트의 Light는 각각 앞왼쪽(LED1:GPIO26), 앞오른쪽(LED2:GPIO16), 뒷왼쪽(LED3:GPIO20), 뒷오른쪽(LED4:GPIO21) 이다.

> 여담으로 전력문제가 가끔씩 문제가 되는 데 전력문제를 쉽게 체크하기 위해 다음 코드를 쓰면 쉽게 알 수 있다.            
> <code>cat /sys/devices/platform/leds/leds/led1/brightness</code>        
> 255면 전력 충분, 0이거나 그 아래라면 전력이 부족하다는 소리이다.

다음 코드는 LED가 잘 작동되는 지 확인하고, 문제없이 잘 작동되는 지 확인한 코드이다.     
$책에 나온 코드와는 조금 다르고 응용하여 만든 예제 코드임$

### 3-1-1.py

<pre>
<code>
import RPi.GPIO as gpio
import time
import sys
import warnings
#warnings.filterwarnings('ignore')

gpio.setwarnings(False)
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

try:
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
           
except KeyboardInterrupt:
    pass
finally:
    gpio.cleanup()
</code>
</pre>

## 3-2. 버튼 입력받기

자동차 키트에 LED 4개 말고도 버튼 4개가 탑재되어 있다.     
앞쪽 보드에서 그 버튼 4개를 확인할 수 있다. 

각각 (SW1:GPIO5), (SW2:GPIO6), (SW3:GPIO13), (SW4:GPIO19) 이다.

이 버튼을 눌렀을 땐 1이라고 표시 되지만, 누르지 않았을 때와 누르기 직전 또는 누르고 난 뒤의 상태는 확연히 0으로 표시되지 않는 다.     
그러므로 라즈베리파이의 자체적으로 Pulldown 저항을 달아줘서 인위적으로 1이 아닌 상태는 다 0으로 표현되게 해야한다.      
(반대로 다른 상황에서 Pulldown 저항뿐만 아니라 Pullup 저항을 사용하기도 한다. 라즈베리파이 자체내부적으로 조정가능하다.)

다음 코드를 보고 스위치를 제어 해보자.

### 3-2-1.py
<pre>
<code>
import sys
import RPi.GPIO as gpio
import time

SW1 = 5
SW2 = 6
SW3 = 13
SW4 = 19

gpio.setwarnings(False)
gpio.cleanup()
gpio.setmode(gpio.BCM)

gpio.setup(SW1, gpio.IN, pull_up_down=gpio.PUD_DOWN)
gpio.setup(SW2, gpio.IN, pull_up_down=gpio.PUD_DOWN)
gpio.setup(SW3, gpio.IN, pull_up_down=gpio.PUD_DOWN)
gpio.setup(SW4, gpio.IN, pull_up_down=gpio.PUD_DOWN)

olditem = [0, 0, 0, 0]
newitem = [0, 0, 0, 0]
cnt = [0, 0, 0, 0]
    
try:
    while True:
          newitem[0] = gpio.input(SW1)
          if newitem[0] != olditem[0]:
             olditem[0] = newitem[0]
             if newitem[0] == 1:
                cnt[0] = cnt[0] + 1
                print('SW1 Click', cnt[0], olditem[0])   
             time.sleep(0.2)
          
          newitem[1] = gpio.input(SW2)
          if newitem[1] != olditem[1]:
             olditem[1] = newitem[1]
             if newitem[1] == 1:
                cnt[1] = cnt[1] + 1
                print('SW2 Click', cnt[1], olditem[1])   
             time.sleep(0.2)
             
          newitem[2] = gpio.input(SW3)
          if newitem[2] != olditem[2]:
             olditem[2] = newitem[2]
             if newitem[2] == 1:
                cnt[2] = cnt[2] + 1
                print('SW3 Click', cnt[2], olditem[2])   
             time.sleep(0.2)
             
          newitem[3] = gpio.input(SW4)
          if newitem[3] != olditem[3]:
             olditem[3] = newitem[3]
             if newitem[3] == 1:
                cnt[3] = cnt[3] + 1
                print('SW4 Click', cnt[3], olditem[3])   
             time.sleep(0.2)

except KeyboardInterrupt:
    pass
finally:
    gpio.cleanup()
    sys.exit()
</code>
</pre>
~~사족을 붙인다면, 필자가 해당 코드가 조금 길다고 해서 배열과 for문으로 줄여보려고 했으나 실패하였음~~      
~~한동안 코드를 손에 놔서 그런듯... 2022년 7월 28일~~      

## 3-3. Buzzer로 경적기능 구현하기

Buzzer는 GPIO 12번이다.

### 3-3-1.py
<pre>
<code>
import sys
import RPi.GPIO as gpio
import time

gpio.setwarnings(False)
gpio.cleanup()
gpio.setmode(gpio.BCM)

Buz = 12

gpio.setup(Buz, gpio.OUT)

p = gpio.PWM(Buz, 261) # 261Hz
p.start(50)

try:
    while True:
          p.start(50)
          p.ChangeFrequency(261)
          time.sleep(1)
          p.stop()
          time.sleep(1)        
    
except KeyboardInterrupt:
    pass

p.stop()
gpio.cleanup()
sys.exit()
</code>
</pre>

여기서 261은 Hz, 즉 주파수인데, 이 주파수를 활용하여 음계를 구성할 수 있다.      
다음 표를 보면 자신이 원하는 음악을 만들 수 있을 것이다.      
<img src="https://user-images.githubusercontent.com/64456822/181456919-c55864ad-e296-4afa-92e6-731497456e26.png" width="800px" height="500px"></img>

필자는 [이러한 것](https://github.com/nsj5068/RaspberryPi/blob/master/AI%EC%9E%90%EB%8F%99%EC%B0%A8/Chapter3%20%EC%9E%90%EB%8F%99%EC%B0%A8%EC%9D%98%20%EA%B8%B0%EB%B3%B8%EA%B8%B0%EB%8A%A5%20%EC%9D%B5%ED%9E%88%EA%B8%B0/BuzzerMusic.py)을 ~~만들었다.~~ 실은 Github에서 찾았다. 출처는 해당 코드 가장 상단에 위치하고 있다.

본론으로 들어가서, 경적기능은 앞서 설명한 음악을 만드는 것보다는 쉽다.    
앞서 테스트로 사용한 코드를 가져와서 스위치와 함께 스위치 1번을 누르면 빵빵~하고 울리는 경적을 만들어 보자.

### 3-3-2.py
<pre>
<code>
import sys
import RPi.GPIO as gpio
import time

Buz = 12
SW1 = 5

gpio.setwarnings(False)
gpio.cleanup()
gpio.setmode(gpio.BCM)
gpio.setup(Buz, gpio.OUT)
gpio.setup(SW1, gpio.IN, pull_up_down=gpio.PUD_DOWN)

p = gpio.PWM(Buz, 391) # 솔
p.stop(50)

oldSw = 0
newSw = 0

try:
    while True:
          newSw = gpio.input(SW1)
          if newSw != oldSw:
             oldSw = newSw
             if newSw == 1:
                p.start(50)
                p.ChangeFrequency(391)
                time.sleep(0.2)
                
                p.stop()
                time.sleep(0.1)
                
                p.start(50)
                p.ChangeFrequency(391)
                time.sleep(0.2)
                
                p.stop()
                time.sleep(0.1)
                
             time.sleep(0.2)
                     
    
except KeyboardInterrupt:
    pass

p.stop()
gpio.cleanup()
sys.exit()
</code>
</pre>

## 3-4. 모터를 구동하여 자동차 움직이기

해당 키트의 PCB 보드에 삽입된 모터 드라이버는 TB6612이다.      
[사진 자료 출처](https://www.adafruit.com/product/2448)            
<img src="https://user-images.githubusercontent.com/64456822/181492223-5fe637e5-713f-491a-85d7-984ad0efa003.png" width="500px" height="300px"></img>     

듀얼 모터 드라이브로써 2개의 모터를 제어할 수 있다. 총 2채널을 제어하는 셈이다.      
이번에 만드는 자동차는 총 모터가 4개 달려있다. 그러므로,      
왼쪽 모터 2개를 하나의 채널로 이용할 수 있게 전기적으로 연결하고,     
오른쪽 또한 그렇게 전기적으로 이읆으로써, 드라이버 1개만으로도 작동할 수 있게 하였다. 

이러한 작동방식을 볼 때, 이 키트는 자동차보다는 탱크의 무한궤도 방식과 흡사하다.

먼저 왼쪽 모터를 구동하는 코드이다.

### 3-4-1.py
<pre>
<code>
import sys
import time
import RPi.GPIO as gpio

PWMA = 18
AIN1 = 22 #Analog IN
AIN2 = 27

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.setup(PWMA, gpio.OUT)
gpio.setup(AIN1, gpio.OUT)
gpio.setup(AIN2, gpio.OUT)

L_M = gpio.PWM(PWMA, 500)
L_M.start(0)

try:
    while True:
          gpio.output(AIN1, 0)
          gpio.output(AIN2, 1)
          L_M.ChangeDutyCycle(100)
          time.sleep(1)
          
          gpio.output(AIN1, 0)
          gpio.output(AIN2, 1)
          L_M.ChangeDutyCycle(0)
          time.sleep(1)
except KeyboardInterrupt:
    pass
    
gpio.cleanup()
</code>
</pre>

다음은 속도 변경을 하는 코드이다.      
PWM을 이용하면 쉽게 변경을 할 수 있다.

### 3-4-2.py
<pre>
<code>
import sys
import time
import RPi.GPIO as gpio

PWMA = 18
AIN1 = 22 #Analog IN
AIN2 = 27

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.setup(PWMA, gpio.OUT)
gpio.setup(AIN1, gpio.OUT)
gpio.setup(AIN2, gpio.OUT)

L_M = gpio.PWM(PWMA, 500)
L_M.start(0)

try:
    while True:
          gpio.output(AIN1, 0)
          gpio.output(AIN2, 1)
          L_M.ChangeDutyCycle(10)
          time.sleep(1)
          
          gpio.output(AIN1, 0)
          gpio.output(AIN2, 1)
          L_M.ChangeDutyCycle(50)
          time.sleep(1)
          
          gpio.output(AIN1, 0)
          gpio.output(AIN2, 1)
          L_M.ChangeDutyCycle(100)
          time.sleep(1)
          
          gpio.output(AIN1, 0)
          gpio.output(AIN2, 1)
          L_M.ChangeDutyCycle(0)
          time.sleep(1)
except KeyboardInterrupt:
    pass
    
gpio.cleanup()
</code>
</pre>
  
책에선 10%일때는 소리만 나지 작동하지 않는 다고 써있지만, 모터에 따라서 힘이 다른데다가,           
해당 키트를 사서 작동시 10% 출력이어도 잘 작동되었음.

다음은 방향 바꾸기 코드이다.

### 3-4-3.py
<pre>
<code>
import sys
import time
import RPi.GPIO as gpio

PWMA = 18
AIN1 = 22 #Analog IN
AIN2 = 27

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.setup(PWMA, gpio.OUT)
gpio.setup(AIN1, gpio.OUT)
gpio.setup(AIN2, gpio.OUT)

L_M = gpio.PWM(PWMA, 500)
L_M.start(0)

try:
    while True:
          gpio.output(AIN1, 0)
          gpio.output(AIN2, 1)
          L_M.ChangeDutyCycle(10)
          time.sleep(1)
          
          gpio.output(AIN1, 0)
          gpio.output(AIN2, 1)
          L_M.ChangeDutyCycle(50)
          time.sleep(1)
          
          gpio.output(AIN1, 1)
          gpio.output(AIN2, 0)
          L_M.ChangeDutyCycle(50)
          time.sleep(1)
          
          gpio.output(AIN1, 1)
          gpio.output(AIN2, 0)
          L_M.ChangeDutyCycle(10)
          time.sleep(1)
except KeyboardInterrupt:
    pass
    
gpio.cleanup()
</code>
</pre>

오른쪽 모터 부분도 추가를 하면 다음과 같은 코드가 된다.

### 3-4-4.py
<pre>
<code>
import sys
import time
import RPi.GPIO as gpio

PWMA = 18
AIN1 = 22 #A Channel IN
AIN2 = 27 

PWMB = 23
BIN1 = 25 #B Channel IN
BIN2 = 24 

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.setup(PWMA, gpio.OUT)
gpio.setup(AIN1, gpio.OUT)
gpio.setup(AIN2, gpio.OUT)
gpio.setup(PWMB, gpio.OUT)
gpio.setup(BIN1, gpio.OUT)
gpio.setup(BIN2, gpio.OUT)

L_M = gpio.PWM(PWMA, 500)
L_M.start(0)
R_M = gpio.PWM(PWMB, 500)
R_M.start(0)

try:
    while True:
          #Right
          gpio.output(AIN1, 0)
          gpio.output(AIN2, 1)
          L_M.ChangeDutyCycle(20)
          gpio.output(BIN1, 1)
          gpio.output(BIN2, 0)
          R_M.ChangeDutyCycle(20)
          time.sleep(1)
          
          #Left
          gpio.output(AIN1, 1)
          gpio.output(AIN2, 0)
          L_M.ChangeDutyCycle(20)
          gpio.output(BIN1, 0)
          gpio.output(BIN2, 1)
          R_M.ChangeDutyCycle(20)
          time.sleep(1)
          
          #Go
          gpio.output(AIN1, 0)
          gpio.output(AIN2, 1)
          L_M.ChangeDutyCycle(20)
          gpio.output(BIN1, 0)
          gpio.output(BIN2, 1)
          R_M.ChangeDutyCycle(20)
          time.sleep(1)
          
          #Back
          gpio.output(AIN1, 1)
          gpio.output(AIN2, 0)
          L_M.ChangeDutyCycle(20)
          gpio.output(BIN1, 1)
          gpio.output(BIN2, 0)
          R_M.ChangeDutyCycle(20)
          time.sleep(1)
except KeyboardInterrupt:
    pass
    
gpio.cleanup()
</code>
</pre>


## 3-5. 스위치 신호를 입력받아 자동차 조종해보기

앞서 코드를 토대로 스위치 입력을 받아 조종해보자.

### 3-5-1.py
<pre>
<code>
import sys
import time
import RPi.GPIO as gpio

SW1 = 5
SW2 = 6
SW3 = 13
SW4 = 19

PWMA = 18
AIN1 = 22 #A Channel IN
AIN2 = 27 

PWMB = 23
BIN1 = 25 #B Channel IN
BIN2 = 24 

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)

gpio.setup(SW1, gpio.IN, pull_up_down=gpio.PUD_DOWN)
gpio.setup(SW2, gpio.IN, pull_up_down=gpio.PUD_DOWN)
gpio.setup(SW3, gpio.IN, pull_up_down=gpio.PUD_DOWN)
gpio.setup(SW4, gpio.IN, pull_up_down=gpio.PUD_DOWN)

gpio.setup(PWMA, gpio.OUT)
gpio.setup(AIN1, gpio.OUT)
gpio.setup(AIN2, gpio.OUT)

gpio.setup(PWMB, gpio.OUT)
gpio.setup(BIN1, gpio.OUT)
gpio.setup(BIN2, gpio.OUT)

L_M = gpio.PWM(PWMA, 500)
L_M.start(0)
R_M = gpio.PWM(PWMB, 500)
R_M.start(0)

def m_G(speed):
    gpio.output(AIN1, 0)
    gpio.output(AIN2, 1)
    L_M.ChangeDutyCycle(speed)
    gpio.output(BIN1, 0)
    gpio.output(BIN2, 1)
    R_M.ChangeDutyCycle(speed)
    
def m_L(speed):
    gpio.output(AIN1, 1)
    gpio.output(AIN2, 0)
    L_M.ChangeDutyCycle(speed)
    gpio.output(BIN1, 0)
    gpio.output(BIN2, 1)
    R_M.ChangeDutyCycle(speed)

def m_R(speed):
    gpio.output(AIN1, 0)
    gpio.output(AIN2, 1)
    L_M.ChangeDutyCycle(speed)
    gpio.output(BIN1, 1)
    gpio.output(BIN2, 0)
    R_M.ChangeDutyCycle(speed)
    
def m_B(speed):
    gpio.output(AIN1, 1)
    gpio.output(AIN2, 0)
    L_M.ChangeDutyCycle(speed)
    gpio.output(BIN1, 1)
    gpio.output(BIN2, 0)
    R_M.ChangeDutyCycle(speed)
    
def m_Stop():
    gpio.output(AIN1, 0)
    gpio.output(AIN2, 1)
    L_M.ChangeDutyCycle(0)
    gpio.output(BIN1, 0)
    gpio.output(BIN2, 1)
    R_M.ChangeDutyCycle(0)
    

try:
    while True:
          if gpio.input(SW1) == 1:
             print('Go')
             m_G(20)

          elif gpio.input(SW2) == 1:
             print('Right')
             m_R(20)

          elif gpio.input(SW3) == 1:
             print('Left')
             m_L(20)

          elif gpio.input(SW4) == 1:
             print('Back')
             m_B(20)
             
          else:
             print('Stop')
             m_Stop()
             
             
          time.sleep(1)
          
except KeyboardInterrupt:
    pass
    
gpio.cleanup()
</code>
</pre>

## Chapter 3 끝.
## [Chapter 4]()
