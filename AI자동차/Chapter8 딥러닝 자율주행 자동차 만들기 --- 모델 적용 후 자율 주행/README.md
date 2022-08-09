# Chapter 8 딥러닝 자율주행 자동차 만들기 --- 모델 적용 후 자율 주행

먼저 모델 적용하는 법과 주행하는 것을 먼저 설명하겠다.            
후술하겠지만, 저번 Chapter 7과 조금 내용이 이어진다.

먼저 Raspberry Pi에 다음 코드를 실행하여 다운로드를 한다.          

<code>pip3 install tensorflow==1.14.0 </code>                
<code>pip3 install keras==2.2.5 </code>                
<code>pip3 install h5py==2.10.0 </code>                


## 8-1-1.py
<pre>
<code>
import sys
import tensorflow as tf
import numpy as np
import h5py
import tensorflow.keras as keras

print('tensorflow : ', tf.__version__)
print('keras : ', keras.__version__)
print('numpy : ', np.__version__)
print('h5py : ', h5py.__version__)
</code>
</pre>


## 8-2-2.py
<pre>
<code>

</code>
</pre>

### 실패 이후 다시 실험

실험 실패를 하였다.            
원인은 학습 데이터 자체의 문제인 것으로 생각된다.                      
그래서 이번엔 느리게 조종하되 트랙을 좀 더 유연한 트랙으로 바꾸었다. 

|Before|After|
|------|-----|
|![1](https://user-images.githubusercontent.com/64456822/183543734-47ba3824-b1db-4e28-b4f2-a5b174808119.JPG)|![2](https://user-images.githubusercontent.com/64456822/183543760-4c20ccad-9d3d-4815-a9ac-74b289d61db6.JPG)|                   



