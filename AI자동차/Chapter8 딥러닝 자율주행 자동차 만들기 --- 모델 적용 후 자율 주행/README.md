# Chapter 8 딥러닝 자율주행 자동차 만들기 --- 모델 적용 후 자율 주행

### 본인의 실험 기록은 이 [링크](https://github.com/nsj5068/RaspberryPi/tree/master/AI%EC%9E%90%EB%8F%99%EC%B0%A8/%EC%8B%A4%ED%97%98%EA%B8%B0%EB%A1%9D#%EC%8B%A4%ED%97%98-%EA%B8%B0%EB%A1%9D)를 타고 열람 바람.


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



이제 트랙에서 왔다갔다를 손으로 옮겨가며 Angle과, 방향이 정확한지 확인을 해보자.           



> 결과화면                   





## 8-2-3.py





   









