# Chapter 6 딥러닝 자율주행 자동차 만들기 --- 데이터 획득

## 6-1. OpenCV를 활용한 키보드 입력

저번시간에 만들었던 라인트레이서는 카메라가 키트의 CAM2 위치에 있었다.               
이번에는 CAM1 위치에 카메라가 자리해야 한다. 그러므로,         
위치를 옮겨주자.

이 CAM1의 위치는 시점이 실제 운전할때와 비슷한 위치라고 한다.

키보드의 입력값을 확인하는 코드를 먼저 작성한다.

### 6-1-1.py
<pre>
<code>
import sys
import cv2
import RPi.GPIO as gpio
import time

def main():
    cam = cv2.VideoCapture(-1)
    cam.set(3, 640)
    cam.set(4, 480)
    
    while(cam.isOpened()):
        keyValue = cv2.waitKey(10)
        print(str(keyValue))
        
        if keyValue == ord('q'):
           break
           
        _, image = cam.read()
        image = cv2.flip(image, -1)
        cv2.imshow('Original', image)
        
    cv2.destroyAllWindows()
    
if __name__ == '__main__':
   main()
   gpio.cleanup()
</code>
</pre>

-1 이 도배되는 상황에서 VNC로 원격접속하고 있는 컴퓨터의 키보드를 쳐보자.              
위쪽 화살표는 82, 왼쪽 화살표는 81, 오른쪽 화살표는 83, 아래쪽 화살표는 84 가 나온다.            

이 숫자는 키보드의 각 키의 고유의 아스키 코드이며, 컴퓨터마다 차이는 있으나 대체로 이 아스키 코드가 대중적이다.           
![3](https://user-images.githubusercontent.com/64456822/182518585-729211ce-8375-45c4-95df-d700c4cb570f.JPG)

우리는 이 keyCode를 이용해 명령어를 구현할 것이다.

### 6-1-2.py
<pre>
<code>
import sys
import cv2
import RPi.GPIO as gpio
import time

def main():
    cam = cv2.VideoCapture(-1)
    cam.set(3, 640)
    cam.set(4, 480)
    
    while(cam.isOpened()):
        keyValue = cv2.waitKey(10)
        #print(str(keyValue))
        
        if keyValue == ord('q'):
           break
        elif keyValue == 82:
           print("up")
        elif keyValue == 84:
           print("down")
        elif keyValue == 81:
           print("left")
        elif keyValue == 83:
           print("right")
           
           
        _, image = cam.read()
        image = cv2.flip(image, -1)
        cv2.imshow('Original', image)
        
    cv2.destroyAllWindows()
    
if __name__ == '__main__':
   main()
   gpio.cleanup()
</code>
</pre>

> 결과화면                           
> ![2](https://user-images.githubusercontent.com/64456822/182518380-af9d143c-22fd-412f-9282-cbeecd54c972.JPG)

## 6-2. 모델 학습을 위한 이미지 보정



