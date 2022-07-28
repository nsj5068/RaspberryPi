# Chapter 3 --- 자동차의 기본기능 익히기

## 3-1. LED로 전조등 구현해보기

자동차 키트의 Light는 각각 앞왼쪽(LED1:GPIO26), 앞오른쪽(LED2:GPIO16), 뒷왼쪽(LED3:GPIO20), 뒷오른쪽(LED4:GPIO21) 이다.

> 여담으로 전력문제가 가끔씩 문제가 되는 데 전력문제를 쉽게 체크하기 위해 다음 코드를 쓰면 쉽게 알 수 있다.            
> <code>cat /sys/devices/platform/leds/leds/led1/brightness</code>        
> 255면 전력 충분, 0이거나 그 아래라면 전력이 부족하다는 소리이다.

[31test.py](https://github.com/nsj5068/RaspberryPi/blob/master/AI%EC%9E%90%EB%8F%99%EC%B0%A8/Chapter3%20%EC%9E%90%EB%8F%99%EC%B0%A8%EC%9D%98%20%EA%B8%B0%EB%B3%B8%EA%B8%B0%EB%8A%A5%20%EC%9D%B5%ED%9E%88%EA%B8%B0/31test.py)


##

##
