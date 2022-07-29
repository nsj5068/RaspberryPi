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
<img src="https://user-images.githubusercontent.com/64456822/181665103-3be59ca0-ede0-40cb-95f3-d5a489adbb1d.JPG" width="400px" height="300px"></img>


<code>ls -l /dev/serial0 </code>

라즈베리파이 터미널에 위의 코드를 치고 주소를 확인해보자.      
또한, 다음 코드를 작성하여 간단한 통신을 주고 받아보자.


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


