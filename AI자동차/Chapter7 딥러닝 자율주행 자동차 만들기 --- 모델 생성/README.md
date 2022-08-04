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

