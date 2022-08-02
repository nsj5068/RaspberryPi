# Chapter 5. 카메라를 활용한 자율주행 자동차 만들기_OpenCV 활용

## 5-1. 카메라로 영상 확인하기

먼저 카메라를 사용하기 위해 다음 설정을 해주자.

> sudo raspi-config     
> 3.Interface Options     
> 1.Camera (or Legacy Camera : Bullseye Version의 경우)      
> Enabled      
> reboot     

카메라가 원활히 작동되는 지 알기 위해 우리는 [VNC Viewer](https://www.realvnc.com/en/connect/download/viewer/) 를 설치해서 확인해보자      
(여담으로 필자가 사용하는 MobaXterm은 X Window를 지원하기 때문에, VNC를 안해도 카메라 창이 뜨기도 한다. 뜨기도 한다라고 하는 것은,      
사용하는 라이브러리나 카메라 사양에 따라서 안뜨기도 한다는 것이다.)

가끔 이런 오류가 나타나는 데 당황할 필요 없다.       
![1](https://user-images.githubusercontent.com/64456822/182056688-457249f2-33ef-4640-8339-f0eccafeb848.JPG)

알아본 결과, Raspberry Pi 3 B+ Model에서는 추가 패치를 통해 이런 오류를 없앴지만, Raspberry Pi 4 B Model 에서는 이 오류가 다시 나타난 모양이다.      
나중에 VNC Viewer나 Raspberry Pi 재단에서 해결할 테지만, 그 시간을 기다릴 수 는 없으니 빨리 해결하자.     
이것의 문제는 해상도가 지정되지 않아서 나오는 문제이다. 그러므로 우리는 해상도를 지정해주면 금방 해결된다.

> sudo raspi-config       
> 2.Display Options             
> 1.Resolution             
> 원하는 해상도로 선택                 
> reboot               

이제 화면도 해결되었으니 카메라로 사진을 한번 찍어보자.      
사진을 찍는 라이브러리는 대표적으로 이 단원에서 사용할 OpenCV, 또 대중적으로 사용하는 Picamera,      
Bullseye Version 부터 Picamera를 대체하는 libcamera 등등이 있는 데,      
우린 간단한 테스트를 위해 간단한 라이브러리를 쓰도록 하자.     
Cheese 라는 프로그램을 사용해보도록 하자.

<code>sudo apt-get install cheese -y</code>

위의 코드를 터미널창에 쳐 Cheese 를 설치하자.       
VNC Viewer를 키고, 왼쪽 위 시작 버튼을 누르고 Cheese를 찾아보자.      
다음과 같은 화면이 나오면 성공이다.       
![2](https://user-images.githubusercontent.com/64456822/182074016-656f3169-ad0c-4754-8019-33163c110cc3.JPG)

Burst 버튼 옆 작은 버튼이 카메라 전환 버튼인데, 연결된 카메라가 아무것도 뜨질 않으면, 그 버튼을 화면이 나올때까지 누르면 된다고 한다.

Picamera로 WebCam을 자주 만들던 필자로썬 해당 카메라의 문제인지, 라이브러리의 문제인지는 몰라도, 카메라 해상도가 문제가 많고, 흐리게 보인다.         
비디오로 전환해서 본다면, Frame의 수가 확연히 적은게 확인될 정도로 엄청 느리다.

카메라가 180도로 뒤집혀져 있을 텐데, 나중에 사진을 찍고 후보정처리로 뒤집으면 되니, 물리적으로 돌리지 않아도 된다.

## 5-2. OpenCV 설치 및 설치 확인

OpenCV 설치      
<code>pip3 install opencv-python</code>

OpenCV, Tensorflow, keras에 맞는 numpy 버젼으로 설치(원래는 이미 설치되어있음.)             
<code>pip3 install numpy==1.20.2</code>

필요한 라이브러리 설치
<pre>
<code>
  sudo apt-get install libhdf5-dev -y        
  #sudo apt-get install libhdf5-serial-dev -y      
  sudo apt-get install libatlas-base-dev -y       
  sudo apt-get install libjasper-dev -y       
  sudo apt-get install libqtgui4 -y                
  sudo apt-get install libqt4-test -y       
</code>
</pre>

순서대로 설명하자면,

> libhdf5-dev : scientific data를 저장하기 위한 라이브러리             
> libhdf5-serial-dev : 위 라이브러리의 더미 패키지 = 다운로드 해봤자 다운이 안된다는 소리이다.                
> libatlas-base-dev : 선형대수학 소프트웨어                  
> libjasper-dev : 이미지의 코딩 및 조작을 위한 소프트웨어의 집합(모음)                         
> libqtgui4 : UI 프로그램으로 유명한 Qt의 GUI 프로그램(현재는 Qt5가 있다.)                          
> libqt4-test : GUI에 사용되는 위젯들의 모음                

다음은 OpenCV를 이용해 사진을 찍고 180도로 돌려진 사진을 원래대로 돌리자.

### 5-2-1.py
<pre>
<code>
import sys
import cv2

def main():
    camera = cv2.VideoCapture(-1)
    camera.set(3,640)
    camera.set(4,480)
    
    while(camera.isOpened()):
         _, image = camera.read()
         image = cv2.flip(image, -1)
         cv2.imshow('camera test' , image)
         
         if cv2.waitKey(1) == ord('q'):
            break
            
    cv2.destroyAllWindows()
    
if __name__ == '__main__':
   main()
</code>
</pre>

> 결과화면       
> ![3](https://user-images.githubusercontent.com/64456822/182276475-414552e3-8b6d-4f59-86f4-f1516fb44c63.JPG)

조금 전 했던 Cheese와 다르게 프레임이 좋은 걸 알수 있다.                        
(잘 모르겠다면 손을 카메라 앞에서 흔들어보자.)                         
또한 영상이 반대로 나오던게 정상적으로 나오고 있다.                 

## 5-3. OpenCV 라인트레이서 자동차 만들기

흰색 테이프를 붙여서 선을 그리면 된다는 데, 수중에 흰색 테이프는 없고 검정색 절연 테이프만 가지고 있어서,         
검정색 테이프를 붙인 뒤, 색을 반전시켜서 사용하거나, 식을 다르게 하여 하면 될것 같다.

또한, 테이프만 바라보게 하기 위해 카메라를 바닥면을 향하게 한다.      
일단, 저번 코드에서 크기를 다르게 하여 영상을 찍어보자.          

### 5-3-1.py
<pre>
<code>
import sys
import cv2

def main():
    camera = cv2.VideoCapture(0)
    camera.set(3,160)
    camera.set(4,120)
    
    while(camera.isOpened()):
         _, image = camera.read()
         image = cv2.flip(image, -1)
         cv2.imshow('camera test' , image)
         
         if cv2.waitKey(1) == ord('q'):
            break
            
    cv2.destroyAllWindows()
    
if __name__ == '__main__':
   main()
</code>
</pre>

사진을 찍어보고 카메라 각도를 잘 조정해준다.       
또한, 카메라 위쪽 부분에는 라인 인식에 쓸데없는 데이터가 있을 확률이 높기 때문에,       
쓸데없는 데이터를 잘라내고, 유효한 데이터만을 얻어보자.       

### 5-3-2.py
<pre>
<code>
import sys
import cv2
import numpy as np

def main():
    camera = cv2.VideoCapture(0)
    camera.set(3,160)
    camera.set(4,120)
    
    while(camera.isOpened()):
         ret, frame = camera.read()
         frame = cv2.flip(frame, -1)
         cv2.imshow('nomal' , frame)
         
         crop_img = frame[60:120, 0:160]
         cv2.imshow('crop', crop_img)
         
         if cv2.waitKey(1) == ord('q'):
            break
            
    cv2.destroyAllWindows()
    
if __name__ == '__main__':
   main()
</code>
</pre>

> 결과화면                        
> ![5](https://user-images.githubusercontent.com/64456822/182276912-3d44d429-0d29-4d4b-a239-db8a0fb5d6fa.JPG)


깔끔하게 불필요한 것들을 잘라내는 것을 확인할 수 있다.       
이제 이미지 분석을 위해, 이미지 처리를 해보자.       

### 5-3-3.py
<pre>
<code>
import sys
import cv2
import numpy as np

def main():
    camera = cv2.VideoCapture(0)
    camera.set(3,160)
    camera.set(4,120)
    
    while(camera.isOpened()):
         ret, frame = camera.read()
         frame = cv2.flip(frame, -1)
         cv2.imshow('nomal' , frame)
         
         crop_img = frame[60:120, 0:160]
         
         gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
         
         blur = cv2.GaussianBlur(gray, (5,5), 0)
         
         cv2.imshow('crop+gray+blur', blur)
         
         if cv2.waitKey(1) == ord('q'):
            break
            
    cv2.destroyAllWindows()
    
if __name__ == '__main__':
   main()
</code>
</pre>

이제 제일 중요한 과정이 남았다. 이미지 인식을 하기 위해, 임계점을 설정하고 그 이상의 값을 최대값으로 바꾸어 검은색 줄을 찾기 쉽게 변환을 해보자.

### 5-3-4.py
<pre>
<code>
import sys
import cv2
import numpy as np

def main():
    camera = cv2.VideoCapture(0)
    camera.set(3,160)
    camera.set(4,120)
    
    while(camera.isOpened()):
         ret, frame = camera.read()
         frame = cv2.flip(frame, -1)
         cv2.imshow('nomal' , frame)
         
         crop_img = frame[60:120, 0:160]
         
         gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
         
         blur = cv2.GaussianBlur(gray, (5,5), 0)
         
         ret, thresh1 = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY_INV)
         
         cv2.imshow('thresh1', thresh1)
         
         if cv2.waitKey(1) == ord('q'):
            break
            
    cv2.destroyAllWindows()
    
if __name__ == '__main__':
   main()
</code>
</pre>

> 결과화면                 
> ![4](https://user-images.githubusercontent.com/64456822/182276793-ad17963b-42aa-49f3-95b1-7b7ed4f926c2.JPG)

책 내용과 완전히 반대의 색을 가지고 있어서 반전을 한 뒤에 찍어보도록 하겠다.
반전 방법에는 여러 가지가 있는 데,                
아예 이미지를 읽어 올때, 색을 반전시키는 방법,                 
임계점 값을 조정하여 반대로 불러오는 방법이 있다.          

### 5-3-5.py
> 첫번째 방법         
<pre>
<code>
import sys
import cv2
import numpy as np

def main():
    camera = cv2.VideoCapture(0)
    camera.set(3,160)
    camera.set(4,120)
    
    while(camera.isOpened()):
         ret, frame = camera.read()
         ret = 255 - ret
         frame = 255 - frame
         frame = cv2.flip(frame, -1)
         cv2.imshow('nomal' , frame)
         
         crop_img = frame[60:120, 0:160]
         
         gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
         
         blur = cv2.GaussianBlur(gray, (5,5), 0)
         
         ret, thresh1 = cv2.threshold(blur, 150, 255, cv2.THRESH_BINARY_INV)
         
         cv2.imshow('thresh1', thresh1)
         
         if cv2.waitKey(1) == ord('q'):
            break
            
    cv2.destroyAllWindows()
    
if __name__ == '__main__':
   main()
</code>
</pre>

> 결과화면         
> ![6](https://user-images.githubusercontent.com/64456822/182278032-69e04afc-a493-42b1-b9cb-f47fcfc6312d.JPG)

### 5-3-6.py
> 두번째 방법          
<pre>
<code>
import sys
import cv2
import numpy as np

def main():
    camera = cv2.VideoCapture(0)
    camera.set(3,160)
    camera.set(4,120)
    
    while(camera.isOpened()):
         ret, frame = camera.read()
         frame = cv2.flip(frame, -1)
         cv2.imshow('nomal' , frame)
         
         crop_img = frame[60:120, 0:160]
         
         gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
         
         blur = cv2.GaussianBlur(gray, (5,5), 0)
         
         ret, thresh1 = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY)
         
         cv2.imshow('thresh1', thresh1)
         
         if cv2.waitKey(1) == ord('q'):
            break
            
    cv2.destroyAllWindows()
    
if __name__ == '__main__':
   main()
</code>
</pre>

> 결과화면        
> ![7](https://user-images.githubusercontent.com/64456822/182278562-a5350fa6-367d-49d3-9239-c3600383eb0c.JPG)

아무래도 두번째 방법이 제일 편하고 간단하다.

이번 작업에서 다뤄졌던 함수에 대한 설명은 [여기](https://opencv-python.readthedocs.io/en/latest/doc/09.imageThresholding/imageThresholding.html)에                
잘 정리되어 있으니 참고 바란다.

참고로 임계점 값이 어느 설정에 따랐냐에 따라서 각자 다른데, 노이즈를 없애기 위해서 유동적으로 영상을 확인해가며 조정한거다.              
또, 그 환경에 따라서도 노이즈가 발생될 수 있으니, 임계점 값을 잘 설정한 후에 진행해야 한다.

이제 무게중심을 잡기 위해, 즉 선을 따라 중간으로 갈 수 있도록 조치를 해주자.

### 5-3-7.py
<pre>
<code>
import sys
import cv2
import numpy as np

def main():
    camera = cv2.VideoCapture(0)
    camera.set(3,160)
    camera.set(4,120)
    
    while(camera.isOpened()):
         ret, frame = camera.read()
         frame = cv2.flip(frame, -1)
         cv2.imshow('nomal' , frame)
         
         crop_img = frame[60:120, 0:160]
         
         gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
         blur = cv2.GaussianBlur(gray, (5,5), 0)
         ret, thresh1 = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY)
         
         mask = cv2.erode(thresh1, None, iterations=2)
         mask = cv2.dilate(mask, None, iterations=2)
         
         cv2.imshow('mask', mask)
         
         contours, hierarchy = cv2.findContours(mask.copy(), 1, cv2.CHAIN_APPROX_NONE)
         
         if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)
            
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            
            cv2.line(crop_img, (cx, 0), (cx, 720), (255, 0, 0), 1)
            cv2.line(crop_img, (0, cy), (1280, cy), (255, 0, 0), 1)
            
            cv2.drawContours(crop_img, contours, -1, (0, 255, 0), 1)
            
            print(cx)
         
         if cv2.waitKey(1) == ord('q'):
            break
            
    cv2.destroyAllWindows()
    
if __name__ == '__main__':
   main()
</code>
</pre>

> 결과 화면      
> 선이 왼쪽에 있을 때            
> ![9](https://user-images.githubusercontent.com/64456822/182280557-2ea61c4e-d353-4c3c-996d-4be5d8cd3c11.JPG)               
> 선이 오른쪽에 있을 때                    
> ![8](https://user-images.githubusercontent.com/64456822/182280599-0806ed0e-0b58-454d-806c-ec969e509656.JPG)

-------------------------------------------------------------------------------------------------------------
#### 함수에 대한 고찰



-------------------------------------------------------------------------------------------------------------

그럼 이 숫자를 통해 좌회전 시킬지, 우회전 시킬지 명령을 내릴 수 있다.

### 5-3-8.py
<pre>
<code>
import sys
import cv2
import numpy as np

def main():
    camera = cv2.VideoCapture(0)
    camera.set(3,160)
    camera.set(4,120)
    
    while(camera.isOpened()):
         ret, frame = camera.read()
         frame = cv2.flip(frame, -1)
         cv2.imshow('nomal' , frame)
         
         crop_img = frame[60:120, 0:160]
         
         gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
         blur = cv2.GaussianBlur(gray, (5,5), 0)
         ret, thresh1 = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY)
         
         mask = cv2.erode(thresh1, None, iterations=2)
         mask = cv2.dilate(mask, None, iterations=2)
         
         cv2.imshow('mask', mask)
         
         contours, hierarchy = cv2.findContours(mask.copy(), 1, cv2.CHAIN_APPROX_NONE)
         
         if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)
            
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            
            if cx >= 95 and cx <= 125:
               print('Turn Left')
            elif cx >=39 and cx <= 65:
               print('Turn Right')
            else:
               print('go')
         
         if cv2.waitKey(1) == ord('q'):
            break
            
    cv2.destroyAllWindows()
    
if __name__ == '__main__':
   main()
</code>
</pre>

> 결과화면                
> ![10](https://user-images.githubusercontent.com/64456822/182296786-575814f0-de89-4874-b405-91f668179ea7.JPG)             
> ![11](https://user-images.githubusercontent.com/64456822/182296799-fd4960d5-bbd3-4443-93af-1a0e4dfcb7b9.JPG)            
> ![12](https://user-images.githubusercontent.com/64456822/182296828-8e856b6f-7d19-4fb4-9563-9868f6eb1e64.JPG)



