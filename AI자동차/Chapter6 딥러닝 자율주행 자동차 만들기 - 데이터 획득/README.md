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

이 숫자들은 waitKey의 리턴값으로 키보드를 누르면 각 키의 고유의 아스키 코드가 오게된다.         
Program 마다 이 keyCode들이 다르며, OpenCV에서는 81, 82, 83, 84 지만,             
Javascript에서는 37, 38, 39, 40 이다.


아무튼 우리는 이 keyCode를 이용해 명령어를 구현할 것이다.

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

책에서 소개한 모델은 NVIDA에서 개발한 학습모델이다. 이 학습모델을 가지고 딥러닝 자율주행 자동차를 만든다고 한다.

일단 저번 라인트레이서 처럼 불필요한 배경 이미지를 잘라내 주자.

### 6-2-1.py
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
        
        height, _, _ = image.shape
        save_image = image[int(height/2):,:,:]
        cv2.imshow('Save', save_image)
        
    cv2.destroyAllWindows()
    
if __name__ == '__main__':
   main()
   gpio.cleanup()
</code>
</pre>

> 결과화면               
> 카메라가 다음 위치에 맞게 조정하면 된다.                      
> ![4](https://user-images.githubusercontent.com/64456822/182561549-49067be1-39b4-463c-9b23-6a2ff387c516.JPG)

우리가 일반적으로 보기 좋은 형식인 RGB 형식을 인공지능이 학습하기 좋은 YUV형식으로 변환해보자.

### 6-2-2.py
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
        
        height, _, _ = image.shape
        save_image = image[int(height/2):,:,:]
        save_image = cv2.cvtColor(save_image, cv2.COLOR_BGR2YUV)
        cv2.imshow('Save', save_image)
        
    cv2.destroyAllWindows()
    
if __name__ == '__main__':
   main()
   gpio.cleanup()
</code>
</pre>

> 결과화면              
> ![5](https://user-images.githubusercontent.com/64456822/182562499-c94e0e28-1a9d-4ed3-a220-7da278ef25e5.JPG)

이제 이번 이미지 처리의 마지막 단계로 NVIDIA 모델에 딱 맞는 사이즈인 200X66 픽셀로 바꾸고 블러링 하는 작업까지 해보자.

### 6-2-3.py
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
        
        height, _, _ = image.shape
        save_image = image[int(height/2):,:,:]
        save_image = cv2.cvtColor(save_image, cv2.COLOR_BGR2YUV)
        save_image = cv2.GaussianBlur(save_image, (3,3), 0)
        save_image = cv2.resize(save_image, (200, 66))
        cv2.imshow('Save', save_image)
        
    cv2.destroyAllWindows()
    
if __name__ == '__main__':
   main()
   gpio.cleanup()
</code>
</pre>

> 결과화면                        
> ![6](https://user-images.githubusercontent.com/64456822/182563686-acd0410e-9f4d-4be9-846e-edbeef9f04ba.JPG)              

## 6-3. OpenCV 이미지 저장하기

이미지 저장은 간단하다.           
다음 코드를 넣으면 된다.

<code> cv2.imwrite('/home/pi/[파일명]/[파일명]/test.png', image) </code>

그러나 이 방법은 두번째 저장될때, 처음 찍었던 것은 날라가고, 새로운 게 들어오는 식이다.

몇번을 찍어도 새로 저장되는 코드는 다음과 같다.

### 6-3-1.py
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
    
    filepath = "/home/pi/AIAutomachine/Pic/test"
    
    i = 0
    
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
        
        cv2.imwrite("%s_%05d.png" % (filepath, i), image)
        i = i + 1
        
        print('save')
        
        time.sleep(1)
        
        
    cv2.destroyAllWindows()
    
if __name__ == '__main__':
   main()
   gpio.cleanup()
</code>
</pre>

> 결과화면              
> ![7](https://user-images.githubusercontent.com/64456822/182566439-69369368-e37a-4698-b099-7c3405638fff.JPG)           

이런식으로 저장된다.

