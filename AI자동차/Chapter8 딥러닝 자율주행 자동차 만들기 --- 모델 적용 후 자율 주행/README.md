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

Chapter 7에서 만든 모델을 Raspberry Pi에 저장한다.               
"lane_navigation_final.h5" 파일이다.              

## 8-2-2.py
<pre>
<code>
import sys
import tensorflow as tf
import h5py
import numpy as np
from tensorflow.keras.models import load_model
import cv2
import RPi.GPIO as gpio

def img_preprocess(image):
    height, _, _= image.shape
    image = image[int(height/2):,:,:]
    image = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
    image = cv2.GaussianBlur(image, (3,3), 0)
    image = cv2.resize(image, (200, 66))
    image = image / 255
    return image
    
def main():
    cam = cv2.VideoCapture(-1)
    cam.set(3, 640)
    cam.set(4, 480)
    model_path = "/home/pi/AIAutomachine/lane_navogation_final.h5"
    model = load_model(model_path)
    
    carState = "stop"
    
    while(cam.isOpened()):
        keyValue = cv2.waitKey(1)
        
        if keyValue == ord('q'):
           break
           
        _, image = cam.read()
        image = cv2.flip(image, -1)
        cv2.imshow('Original', image)
        
        preprocessed = img_preprocess(image)
        cv2.imshow('pre', preprocessed)
        
        X = np.asarray([preprocessed])
        steering_angle = int(model.predict(X)[0])
        print("predict angle : ", steering_angle)
        
    cv2.destroyAllWindows()
    
    
if __name__ == '__main__':
   main()
   gpio.cleanup()
</code>
</pre>


### 실패

위의 코드를 가지고 실험한 결과, Right라고 판단한 부분이 더 많았다. 이 뒤에 올 코드로 실제 실험도 했으나, 결과는 똑같았다.                       
그러므로, 다음 코드를 가져와 설명하는 것이 아닌 다시 실험을 시작하여, 그 결과를 서술하겠다.             



### 실패 이후 다시 실험
         
원인은 학습 데이터 자체의 문제인 것으로 생각된다.                      
그래서 이번엔 느리게 조종하되 트랙을 좀 더 유연한 트랙으로 바꾸었다. 

|Before|After|
|------|-----|
|![1](https://user-images.githubusercontent.com/64456822/183543734-47ba3824-b1db-4e28-b4f2-a5b174808119.JPG)|![2](https://user-images.githubusercontent.com/64456822/183543760-4c20ccad-9d3d-4815-a9ac-74b289d61db6.JPG)|                   



