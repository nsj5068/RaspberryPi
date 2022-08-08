# Chapter 7 딥러닝 자율주행 자동차 만들기 --- 모델 생성

시작하기에 앞서, 책에서 설명되어 있는 매우 초보적인 설명은 다 넘어가겠다.

## 7-3. 자율 주행 자동차 학습 모델 생성하기

NVIDIA가 만든 모델 답게 런타임 유형을 GPU로 바꾸어야 한다.                   
또한 사용하기에 앞서 구글 드라이브 마운트를 해주자.       

다음 코드를 또 실행한다. 책에서는 라즈베리파이와 호환되게 낮춰준다고 한다. 왜 낮추는 지에 대해서 검색을 해보았는 데,       
여러 결과를 보고 납득하였다.                   
[결과1](https://qengineering.eu/install-tensorflow-2.2.0-on-raspberry-pi-4.html)

> !pip uninstall tensorflow -y                
> !pip install tensorflow==1.14                
> !pip uninstall keras -y                 
> !pip install keras==2.2.5                 
> !pip install h5py==2.10.0                        



설정을 다 한 뒤에 런타임 도구 항목에 들어가서 런타임 다시 시작을 누른다.            
설정을 적용하기 위해서이다.            
다음 코드를 실행한다.          

## 7-3-1.py
<pre>
<code>

</code>
</pre>


import tensorflow.keras 에서 문제가 생기는 데 다음 링크를 타고 보면 문제의 원인을 알 수 있다.

[오류](https://stackoverflow.com/questions/71000250/import-tensorflow-keras-could-not-be-resolved-after-upgrading-to-tensorflow-2)                



실험을 오래 하다보니 [이러한 문제](https://limitsinx.tistory.com/135)가 생겼는 데 찾아보니....                
기다리거나, 돈을 내서 돌리는 수밖에 없다고 한다....






