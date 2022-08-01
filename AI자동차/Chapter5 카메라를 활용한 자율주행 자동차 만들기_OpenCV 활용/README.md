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
<code>pip3 install numpy==1.20.3</code>

필요한 라이브러리 설치
<pre>
<code>
  sudo apt-get install libhdf5-dev -y        
  sudo apt-get install libhdf5-serial-dev -y      
  sudo apt-get install libatlas-base-dev -y       
  sudo apt-get install libjasper-dev -y       
  sudo apt-get install libqtgui4 -y                
  sudo apt-get install libqt4-test -y       
</code>
</pre>

순서대로 설명하자면,

> libhdf5-dev : scientific data를 저장하기 위한 라이브러리         
> libhdf5-serial-dev : 위 라이브러리의 더미 패키지        
> libatlas-base-dev : 선형대수학 소프트웨어
> libjasper-dev : 이미지의 코딩 및 조작을 위한 소프트웨어의 집합(모음)
> libqtgui4 : UI 프로그램으로 유명한 Qt의 GUI 프로그램(현재는 Qt5가 있다.)
> libqt4-test : GUI에 사용되는 위젯들의 모음



