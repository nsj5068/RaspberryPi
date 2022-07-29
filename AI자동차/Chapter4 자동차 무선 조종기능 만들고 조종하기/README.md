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

> 한줄씩 받기

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

> 문자열로 받기

<pre>
<code>
import sys
import serial

BLESerial = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1.0)

try:
     while True:
           data = BLESerial.readline()
           data.decode()
           print(data)
           
except KeyboardInterrupt:
     pass
     
BLESerial.close()
</code>
</pre>

> 문자열 찾기 및 조건문 실행

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
              print("Ok "+ data)
           elif data.find("right") >= 0:
              print("Ok " + data)
           elif data.find("stop") >= 0:
              print("Ok " + data)
                  
           
except KeyboardInterrupt:
     pass
     
BLESerial.close()
</code>
</pre>

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






