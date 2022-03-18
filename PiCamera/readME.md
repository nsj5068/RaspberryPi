# 라즈베리 파이 buster 버젼 이후의 Bullseye 버젼 부터 다음 설명을 참고.
## PiCamera는 Bullseye 버젼에선 호환되지 않는 다. 굳이 쓴다면 레거시 OS를 불러와 사용해야함. 
## 이제는 libcamera를 이용한 PiCamera2 라이브러리를 써야만 한다.


[참고링크] : https://www.robotstory.co.kr/london/?vid=244

호환 라즈베리파이 카메라 모듈 : V1/V2/HQ

### 대체적으로 ssh를 이용한 putty나 XWindown를 지원하는 MobaXterm도 해당 라이브러리를 사용하면 실행되지 않으니 주의할 것.
### VNC Viewr를 사용하여 실행할 것.

오류1 : https://forums.raspberrypi.com/viewtopic.php?t=326315 \
오류2 : https://github.com/Motion-Project/motion/issues/1434 \
오류3 : https://raspberrypi.stackexchange.com/questions/135364/libcamera-stack-does-not-work-with-bullseye \
오류4 : https://forums.raspberrypi.com/viewtopic.php?p=1958297

또는 github를 통해 Picamera2를 사용 \
[참고링크] : https://github.com/raspberrypi/picamera2 \
[참고링크] : https://www.raspberrypi.com/news/a-preview-release-of-the-picamera2-library/ 

