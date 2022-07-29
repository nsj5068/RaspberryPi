# Chapter4 자동차 무선 조종기능 만들고 조종하기

## 4-1. Bluetooth Serial 통신으로 데이터 주고 받기

참고로 현재 사용되는 Serial 통신으로 Raspberry Pi와 Arduino간에도 통신이 가능하다.

키트에 포함된 Bluetooth HM-10 모델로 실험해보자.

> 1. sudo raspi-config                       
> 2. Interface Option 찾기 및 Enter            
> 3. Serial Port 찾기 및 Enter                
> 4. Enable? 라고 뜨는 데, Yes 
> ----------------------------------------------------------------------------
> 2022년 7월 29일
> 5. [Errno 13] could not open port /dev/ttyS0: [Errno 13] Permission denied: '/dev/ttyS0'
> 이런식으로 하면 이 오류가 뜬다.
> 6. 정확한 순서는 Serial Port를 찾고서 Enter
> 7. Login Console은 비활성화, Serial Port는 활성화 해주면 된다.
> 8. Reboot

스마트폰에서는 스토어에 들어가 "Serial Bluetooth Terminal"을 다운 받는 다.      

![1](https://user-images.githubusercontent.com/64456822/181665298-e11f7931-da7b-46fc-ac62-d222e19d411d.JPG)
![2](https://user-images.githubusercontent.com/64456822/181665317-79bf0c46-f655-436f-8301-559a6be03ebb.JPG)
![3](https://user-images.githubusercontent.com/64456822/181665327-24c1be4a-6a9b-4e8e-a67b-86b84be86fec.JPG)
![4](https://user-images.githubusercontent.com/64456822/181665342-1e5a265a-eaec-40ed-9b89-9ded863d5a4b.JPG)

처음 사용한다면 초기 블루투스 명이, "MLT-BT05, HM-10, BT05" 등의 이름으로 검색된다.



라즈베리파이 터미널에 아래의 코드를 치고 주소를 확인해보자.      
또한, 다음 코드를 작성하여 간단한 통신을 주고 받아보자.

<code>ls -l /dev/serial0 </code>

<pre>
<code>
import sys
import serial

BLESerial = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1.0)

try:
     while True:
           data = BLESerial.read()
           print(data)
           
except KeyboardInterrupt:
     pass
     
BLESerial.close()
</code>
</pre>

> 결과화면
> 
> ![5](https://user-images.githubusercontent.com/64456822/181665584-8616f0f6-0e9f-442a-ba57-ce9b5ac43a44.JPG)

아직 아무것도 보내지 않은 상태다.      
또 값을 받을때, "b''" 라고 오는 데, Bytes 형식으로 왔다는 소리이다.     
이것은 추후, 문자열을 주고 받거나 숫자를 받을 때 문제가 있을 수 있기 때문에,      
Python에선 Encode와 Decode를 해줘야 한다.

> 결과화면
> 
> ![6](https://user-images.githubusercontent.com/64456822/181666584-10b35a26-629d-4ed0-b14c-49baea3fd085.JPG)
> ![8](https://user-images.githubusercontent.com/64456822/181666611-23e724d4-c39d-4cdb-bad1-dc13ef5f6b2f.JPG)
> 
> ![7](https://user-images.githubusercontent.com/64456822/181666597-e533acc6-04d6-4f3e-a3f5-e3c10fdb1f18.JPG)

'\r', '\n' 이 나오는 이유는 줄바꿈을 하기 위해서이다.      
즉 문장이 끝났다는 것을 알리기 위해 자동으로 붙여준다.      
앞서 말했다시피 이러한 것은 원활한 통신에 방해되기 때문에, Python 상에서         
데이터를 보낼때, Encode를 하고, 받을 때도 Decode를 하여 받아야 한다.       

## 4-2. Serial Data 분석하여 명령어 해석하기

이 단원에서는 딱히 설명할 필요는 없고, 굳이 알고 싶은 사람이 있다면,        
pyserial 이나, Serial Library Document 들을 찾아서 보시길 바란다.

#### 한줄씩 받기

<pre>
<code>
import sys
import serial

BLESerial = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1.0)

try:
     while True:
           data = BLESerial.readline()
           print(data)
           
except KeyboardInterrupt:
     pass
     
BLESerial.close()
</code>
</pre>
> 결과화면          
> ![9](https://user-images.githubusercontent.com/64456822/181691868-d9c320e4-14ed-4abb-ab01-827a4a8d675c.JPG)



#### 문자열로 받기

<pre>
<code>
import sys
import serial

BLESerial = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1.0)

try:
     while True:
           data = BLESerial.readline()
           data = data.decode()
           print(data)
           
except KeyboardInterrupt:
     pass
     
BLESerial.close()
</code>
</pre>
> 결과화면                 
> ![10](https://user-images.githubusercontent.com/64456822/181692170-2255b900-fe5e-4d8c-90d9-4837c064e491.JPG)


#### 문자열 찾기 및 조건문 실행

<pre>
<code>
import sys
import serial

BLESerial = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1.0)

try:
     while True:
           data = BLESerial.readline()
           data = data.decode()
           if data.find("go") >= 0:
              print("Ok " + data)
           elif data.find("back") >= 0:
              print("Ok " + data)
           elif data.find("left") >= 0:
              print("Ok " + data)
           elif data.find("right") >= 0:
              print("Ok " + data)
           elif data.find("stop") >= 0:
              print("Ok " + data)
                  
           
except KeyboardInterrupt:
     pass
     
BLESerial.close()
</code>
</pre>
> 결과화면                        
> ![12](https://user-images.githubusercontent.com/64456822/181692665-1e0ea17c-cc1f-4b15-9aef-087e13bbfb42.JPG)                
> ![11](https://user-images.githubusercontent.com/64456822/181692680-aca2dfcb-f02c-419c-8ff6-34b22b02081e.JPG)



## 4-3. Thread를 활용하여 통신기능 분리하기

쉽게 말해 데이터를 받을 때까지 기다리는 단방향 통신에서, 동시에 다른 프로그램을 실행시킬수 있는,       
단방향 통신이 되는 것이다.       
~~엄밀히 말해 양방향 통신은 아니다...~~

이제 분리하는 코드를 만들어보자.

<pre>
<code>
import sys
import serial
import time
import threading

BLESerial = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1.0)

gdata = " "

def serial_decode():
    global gdata
    while True:
          data = BLESerial.readline()
          data = data.decode()
          gdata = data
          
def main():
    global gdata
    try:
        while True:
              print("data : " + gdata)
              time.sleep(1.0)
              
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
         task1 = threading.Thread(target=serial_decode)
         task1.start()
         main()
         BLESerial.close()
</code>
</pre>

중간에 정지시킬 경우 실행되고 있던 Thread가 마저 종료되지 않고 중간에 종료되서 오류가 생길 수 있다.     
굳이 신경쓸 정도는 아니지만, 신경이 쓰인다면, Thread를 Daemon Thread로 만들거나,       
sys.exit()으로 Main Thread를 종료시켜 나머지 Sub Thread까지 한꺼번에 종료되는 식으로 만들 수 있다.

## 4-4. BLE Serial 통신으로 조종하는 자동차 만들기
## + 4-5. 스위치를 이용한 비상정지 버튼 

앞서 4-2에서 마지막으로 했던 "[문자열 찾기 및 조건문 실행](https://github.com/nsj5068/RaspberryPi/blob/master/AI%EC%9E%90%EB%8F%99%EC%B0%A8/Chapter4%20%EC%9E%90%EB%8F%99%EC%B0%A8%20%EB%AC%B4%EC%84%A0%20%EC%A1%B0%EC%A2%85%EA%B8%B0%EB%8A%A5%20%EB%A7%8C%EB%93%A4%EA%B3%A0%20%EC%A1%B0%EC%A2%85%ED%95%98%EA%B8%B0/README.md#%EB%AC%B8%EC%9E%90%EC%97%B4-%EC%B0%BE%EA%B8%B0-%EB%B0%8F-%EC%A1%B0%EA%B1%B4%EB%AC%B8-%EC%8B%A4%ED%96%89)" 에서 코드를 가져와 응용하여,      
자동차를 조종해보자.

<pre>
<code>
import sys
import serial
import threading

BLESerial = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1.0)

gData = ""

def serial_decode():
    global gData
    while True:
          data = BLESerial.readline()
          data = data.decode()
          gData = data

def main():
    global gData
    try:
        while True:
           if gData.find("go") >= 0:
              print("Ok " + gData)
              gData = ""
           elif gData.find("back") >= 0:
              print("Ok " + gData)
              gData = ""
           elif gData.find("left") >= 0:
              print("Ok "+ gData)
              gData = ""
           elif gData.find("right") >= 0:
              print("Ok " + gData)
              gData = ""
           elif gData.find("stop") >= 0:
              print("Ok " + gData)
              gData = ""
              
    except KeyboardInterrupt:
        pass
     
if __name__ == '__main__':
         task1 = threading.Thread(target=serial_decode)
         task1.start()
         main()
         BLESerial.close()
</code>
</pre>

> 결과 화면
> ![14](https://user-images.githubusercontent.com/64456822/181703429-56aaa144-903a-4493-ba5c-5fb738299316.JPG)       
> 아래 버튼이 변경된 것을 알 수 있는 데, 바로 단축키 기능이다.       
> 본래 M1~M7로 버튼을 꾹누르면 단축키를 지정할 수 있다.          
> ![13](https://user-images.githubusercontent.com/64456822/181703648-ff5e90df-0744-4b03-b465-beabed9c4c23.JPG)

블루투스로 명령을 내리는 법까지 알게 되었으니 저번 Chapter3에서 했던 코드를 가져와 원격으로 조종하는 코드를 만들어 보자.

<pre>
<code>
import sys
import time
import RPi.GPIO as gpio
import serial
import threading

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

BLESerial = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1.0)

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

gData = ""

def serial_decode():
    global gData
    while True:
          data = BLESerial.readline()
          data = data.decode()
          gData = data

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
    
def main():
    global gData
    try:
        while True:
           if gData.find("go") >= 0:
              print("Ok " + gData)
              gData = ""
              m_G(30)
           elif gData.find("back") >= 0:
              print("Ok " + gData)
              gData = ""
              m_B(30)
           elif gData.find("left") >= 0:
              print("Ok "+ gData)
              gData = ""
              m_L(30)
           elif gData.find("right") >= 0:
              print("Ok " + gData)
              gData = ""
              m_R(30)
           elif gData.find("stop") >= 0:
              print("Ok " + gData)
              gData = ""
              m_Stop()
           
           if gpio.input(SW1) == 1 or gpio.input(SW2) == 1 or gpio.input(SW3) == 1 or gpio.input(SW4) == 1:
              m_Stop()
              
    except KeyboardInterrupt:
        pass
    
if __name__ == '__main__':
         task1 = threading.Thread(target=serial_decode)
         task1.start()
         main()
         BLESerial.close()
         gpio.cleanup()
</code>
</pre>

자동차가 정상작동 되는 것을 확인할 수 있다.      
작동 중 스위치를 누르면 비상정지 되는 것도 확인 가능하다. 

## 4-6. 이동방향 LED로 표시하기

Chapter3에서 했던 LED 작동 코드를 가져와서 쉽게 코딩해보자.       
이번에 하는 것은 자동차 등처럼 앞으로 갈땐 전조등처럼 앞 2개를 밝히고, 후진할땐 실제로 자동차에 후진기어를 넣었을 때,       
뒤에 등이 들어오는 것처럼 코딩하는 것이다.

<pre>
<code>
import sys
import time
import RPi.GPIO as gpio
import serial
import threading

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

LED1 = 26
LED2 = 16
LED3 = 20
LED4 = 21

BLESerial = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1.0)

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)

#Switch
gpio.setup(SW1, gpio.IN, pull_up_down=gpio.PUD_DOWN)
gpio.setup(SW2, gpio.IN, pull_up_down=gpio.PUD_DOWN)
gpio.setup(SW3, gpio.IN, pull_up_down=gpio.PUD_DOWN)
gpio.setup(SW4, gpio.IN, pull_up_down=gpio.PUD_DOWN)

#Motor Driver Ch1
gpio.setup(PWMA, gpio.OUT)
gpio.setup(AIN1, gpio.OUT)
gpio.setup(AIN2, gpio.OUT)

#Motor Driver Ch2
gpio.setup(PWMB, gpio.OUT)
gpio.setup(BIN1, gpio.OUT)
gpio.setup(BIN2, gpio.OUT)

#LED
gpio.setup(LED1, gpio.OUT)
gpio.setup(LED2, gpio.OUT)
gpio.setup(LED3, gpio.OUT)
gpio.setup(LED4, gpio.OUT)

#Motor
L_M = gpio.PWM(PWMA, 500)
L_M.start(0)
R_M = gpio.PWM(PWMB, 500)
R_M.start(0)

gData = ""

def serial_decode():
    global gData
    while True:
          data = BLESerial.readline()
          data = data.decode()
          gData = data

def m_G(speed):
    gpio.output(AIN1, 0)
    gpio.output(AIN2, 1)
    L_M.ChangeDutyCycle(speed)
    gpio.output(BIN1, 0)
    gpio.output(BIN2, 1)
    R_M.ChangeDutyCycle(speed)
    gpio.output(LED1, gpio.HIGH)
    gpio.output(LED2, gpio.HIGH)
    gpio.output(LED3, gpio.LOW)
    gpio.output(LED4, gpio.LOW)
    
def m_L(speed):
    gpio.output(AIN1, 1)
    gpio.output(AIN2, 0)
    L_M.ChangeDutyCycle(speed)
    gpio.output(BIN1, 0)
    gpio.output(BIN2, 1)
    R_M.ChangeDutyCycle(speed)
    gpio.output(LED1, gpio.HIGH)
    gpio.output(LED2, gpio.LOW)
    gpio.output(LED3, gpio.HIGH)
    gpio.output(LED4, gpio.LOW)

def m_R(speed):
    gpio.output(AIN1, 0)
    gpio.output(AIN2, 1)
    L_M.ChangeDutyCycle(speed)
    gpio.output(BIN1, 1)
    gpio.output(BIN2, 0)
    R_M.ChangeDutyCycle(speed)
    gpio.output(LED1, gpio.LOW)
    gpio.output(LED2, gpio.HIGH)
    gpio.output(LED3, gpio.LOW)
    gpio.output(LED4, gpio.HIGH)
    
def m_B(speed):
    gpio.output(AIN1, 1)
    gpio.output(AIN2, 0)
    L_M.ChangeDutyCycle(speed)
    gpio.output(BIN1, 1)
    gpio.output(BIN2, 0)
    R_M.ChangeDutyCycle(speed)
    gpio.output(LED1, gpio.LOW)
    gpio.output(LED2, gpio.LOW)
    gpio.output(LED3, gpio.HIGH)
    gpio.output(LED4, gpio.HIGH)
    
def m_Stop():
    gpio.output(AIN1, 0)
    gpio.output(AIN2, 1)
    L_M.ChangeDutyCycle(0)
    gpio.output(BIN1, 0)
    gpio.output(BIN2, 1)
    R_M.ChangeDutyCycle(0)
    gpio.output(LED1, gpio.LOW)
    gpio.output(LED2, gpio.LOW)
    gpio.output(LED3, gpio.LOW)
    gpio.output(LED4, gpio.LOW)
    
def main():
    global gData
    try:
        while True:
           if gData.find("go") >= 0:
              print("Ok " + gData)
              gData = ""
              m_G(30)
           elif gData.find("back") >= 0:
              print("Ok " + gData)
              gData = ""
              m_B(30)
           elif gData.find("left") >= 0:
              print("Ok "+ gData)
              gData = ""
              m_L(30)
           elif gData.find("right") >= 0:
              print("Ok " + gData)
              gData = ""
              m_R(30)
           elif gData.find("stop") >= 0:
              print("Ok " + gData)
              gData = ""
              m_Stop()
           
           if gpio.input(SW1) == 1 or gpio.input(SW2) == 1 or gpio.input(SW3) == 1 or gpio.input(SW4) == 1:
              m_Stop()
              
    except KeyboardInterrupt:
        pass
    
if __name__ == '__main__':
         task1 = threading.Thread(target=serial_decode)
         task1.start()
         main()
         BLESerial.close()
         gpio.cleanup()
</code>
</pre>

LED 또한 정상 작동 되며, 설계한 방향대로 잘 작동되는 것을 확인할 수 있다.
좀 더 발전된 Version을 만들고 싶다면, 실제 자동차처럼 왼쪽과 오른쪽의 방향지시등을 점멸하는 것처럼 이 키트에도 적용해보도록 해보자.

--------------------------------------------------------------------------------------------------------------------------
2022년 7월 29일

위의 방향지시등을 구현하기 위해 Thread를 사용하여 구현해보았으나, 작동이 잘 되지 않음.     
concurrent.futures 함수를 도입해볼까 했지만 아직은 이해불가. 
아래 4-7은 29일에 끝마치겠으나 방향지시등 예제는 좀 더 연구를 해보도록 하겠음.

--------------------------------------------------------------------------------------------------------------------------

<pre>
<code>

</code>
</pre>

## 4-7 Buzzer를 이용하여 경적기능 추가하기

이것또한 Chapter3에서 했던 Buzzer 코드를 응용하여 금세 적용시킬수 있다.

<pre>
<code>
import sys
import time
import RPi.GPIO as gpio
import serial
import threading

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

LED1 = 26
LED2 = 16
LED3 = 20
LED4 = 21

Buz = 12

BLESerial = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1.0)

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)

#Switch
gpio.setup(SW1, gpio.IN, pull_up_down=gpio.PUD_DOWN)
gpio.setup(SW2, gpio.IN, pull_up_down=gpio.PUD_DOWN)
gpio.setup(SW3, gpio.IN, pull_up_down=gpio.PUD_DOWN)
gpio.setup(SW4, gpio.IN, pull_up_down=gpio.PUD_DOWN)

#Motor Driver Ch1
gpio.setup(PWMA, gpio.OUT)
gpio.setup(AIN1, gpio.OUT)
gpio.setup(AIN2, gpio.OUT)

#Motor Driver Ch2
gpio.setup(PWMB, gpio.OUT)
gpio.setup(BIN1, gpio.OUT)
gpio.setup(BIN2, gpio.OUT)

#LED
gpio.setup(LED1, gpio.OUT)
gpio.setup(LED2, gpio.OUT)
gpio.setup(LED3, gpio.OUT)
gpio.setup(LED4, gpio.OUT)

#Buzzer
gpio.setup(Buz, gpio.OUT)

p = gpio.PWM(Buz, 391) # 솔
p.stop(50)

#Motor
L_M = gpio.PWM(PWMA, 500)
L_M.start(0)
R_M = gpio.PWM(PWMB, 500)
R_M.start(0)

gData = ""

def serial_decode():
    global gData
    while True:
          data = BLESerial.readline()
          data = data.decode()
          gData = data

def m_G(speed):
    gpio.output(AIN1, 0)
    gpio.output(AIN2, 1)
    L_M.ChangeDutyCycle(speed)
    gpio.output(BIN1, 0)
    gpio.output(BIN2, 1)
    R_M.ChangeDutyCycle(speed)
    gpio.output(LED1, gpio.HIGH)
    gpio.output(LED2, gpio.HIGH)
    gpio.output(LED3, gpio.LOW)
    gpio.output(LED4, gpio.LOW)
    
def m_L(speed):
    gpio.output(AIN1, 1)
    gpio.output(AIN2, 0)
    L_M.ChangeDutyCycle(speed)
    gpio.output(BIN1, 0)
    gpio.output(BIN2, 1)
    R_M.ChangeDutyCycle(speed)
    gpio.output(LED1, gpio.HIGH)
    gpio.output(LED2, gpio.LOW)
    gpio.output(LED3, gpio.HIGH)
    gpio.output(LED4, gpio.LOW)

def m_R(speed):
    gpio.output(AIN1, 0)
    gpio.output(AIN2, 1)
    L_M.ChangeDutyCycle(speed)
    gpio.output(BIN1, 1)
    gpio.output(BIN2, 0)
    R_M.ChangeDutyCycle(speed)
    gpio.output(LED1, gpio.LOW)
    gpio.output(LED2, gpio.HIGH)
    gpio.output(LED3, gpio.LOW)
    gpio.output(LED4, gpio.HIGH)
    
def m_B(speed):
    gpio.output(AIN1, 1)
    gpio.output(AIN2, 0)
    L_M.ChangeDutyCycle(speed)
    gpio.output(BIN1, 1)
    gpio.output(BIN2, 0)
    R_M.ChangeDutyCycle(speed)
    gpio.output(LED1, gpio.LOW)
    gpio.output(LED2, gpio.LOW)
    gpio.output(LED3, gpio.HIGH)
    gpio.output(LED4, gpio.HIGH)
    
def m_Stop():
    gpio.output(AIN1, 0)
    gpio.output(AIN2, 1)
    L_M.ChangeDutyCycle(0)
    gpio.output(BIN1, 0)
    gpio.output(BIN2, 1)
    R_M.ChangeDutyCycle(0)
    gpio.output(LED1, gpio.LOW)
    gpio.output(LED2, gpio.LOW)
    gpio.output(LED3, gpio.LOW)
    gpio.output(LED4, gpio.LOW)
    p.stop()
    
def main():
    global gData
    try:
        while True:
           if gData.find("go") >= 0:
              print("Ok " + gData)
              gData = ""
              m_G(30)
           elif gData.find("back") >= 0:
              print("Ok " + gData)
              gData = ""
              m_B(30)
           elif gData.find("left") >= 0:
              print("Ok "+ gData)
              gData = ""
              m_L(30)
           elif gData.find("right") >= 0:
              print("Ok " + gData)
              gData = ""
              m_R(30)
           elif gData.find("stop") >= 0:
              print("Ok " + gData)
              gData = ""
              m_Stop()
           elif gData.find("bz_on") >= 0:
              print("Ok " + gData)
              gData = ""
              p.start(50)
              p.ChangeFrequency(391)
           elif gData.find("bz_off") >= 0:
              print("Ok " + gData)
              gData = ""
              p.stop()
              p.ChangeFrequency(391)
           
           if gpio.input(SW1) == 1 or gpio.input(SW2) == 1 or gpio.input(SW3) == 1 or gpio.input(SW4) == 1:
              m_Stop()
              
              
    except KeyboardInterrupt:
        pass
    
if __name__ == '__main__':
         task1 = threading.Thread(target=serial_decode)
         task1.start()
         main()
         BLESerial.close()
         gpio.cleanup()
</code>
</pre>

## 4-8. Raspberry Pi 부팅시 자동으로 코드 실행

부팅시 자동으로 코드를 실행하는 방법은 여러가지가 있다.      
init.d 디렉토리를 사용하는 방법, systemd를 사용하는 방법, Crontab을 사용하는 방법, .bashrc 파일을 건드리는 법 등 다양한 방법이 있는 데,      
책에서 설명하는 방법은 다음과 같다.

<code>sudo nano /etc/xdg/lxsession/LXDE-pi/autostart</code>

이 코드를 터미널에 친 다음, autostart 파일의 맨 끝으로 커서를 내린다.     
맨 마지막줄에, 다음 내용을 추가하고 저장한 뒤, reboot 시키면 자동으로 부팅시 프로그램이 실행되는 것을 확인할 수 있다.     
(리부트 방법: sudo reboot)

<code>lxterminal -e sudo python3 /home/pi/[your_directory]/47test.py</code>

자동실행을 끝내고 싶다면, 다시 해당 파일을 열고 전에 추가한 내용을 지우고 저장하고 리부트 하면 된다.
