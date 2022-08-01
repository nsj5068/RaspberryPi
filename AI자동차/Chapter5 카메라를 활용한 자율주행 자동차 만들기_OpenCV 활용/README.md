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


