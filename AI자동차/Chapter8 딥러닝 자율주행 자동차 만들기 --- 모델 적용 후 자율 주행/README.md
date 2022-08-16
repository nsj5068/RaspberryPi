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



## 8-3-1.py
<pre>
<code>
import cv2
import tensorflow as tf
import h5py
import numpy as np
from tensorflow.keras.models import load_model
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
    model_path = "/home/pi/AIAutomachine/lane_navogation_final2.h5"
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
        
        if steering_angle >= 85 and steering_angle <= 95:
           print('go')
        elif steering_angle > 96 :
           print('right')
        elif steering_angle < 84 :
           print('left')
        
    cv2.destroyAllWindows()
    
    
if __name__ == '__main__':
   main()
   gpio.cleanup()
</code>
</pre>

> 결과화면               
> ![1](https://user-images.githubusercontent.com/64456822/184805929-6e1d6022-bdcb-4e6c-beaf-dc2193980bf7.JPG)                       
> ![2](https://user-images.githubusercontent.com/64456822/184805953-6c6590a8-3273-4548-a2fc-e4225eac23fb.JPG)                      
> ![3](https://user-images.githubusercontent.com/64456822/184805974-92de8d93-22db-45e8-b14c-744705801250.JPG)                


이것까지만 하면 실질적 Test는 다 끝났다.           
다음은 실제 AI 주행을 해보는 거다.           



## 8-4-1.py
<pre>
<code>
import cv2
import tensorflow as tf
import h5py
import numpy as np
from tensorflow.keras.models import load_model
import RPi.GPIO as gpio

PWMA = 18
AIN1 = 22 #A Channel IN
AIN2 = 27 

PWMB = 23
BIN1 = 25 #B Channel IN
BIN2 = 24 

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)

gpio.setup(PWMA, gpio.OUT)
gpio.setup(AIN1, gpio.OUT)
gpio.setup(AIN2, gpio.OUT)

gpio.setup(PWMB, gpio.OUT)
gpio.setup(BIN1, gpio.OUT)
gpio.setup(BIN2, gpio.OUT)

L_M = gpio.PWM(PWMA, 500)
L_M.start(0)
R_M = gpio.PWM(PWMB, 500)
R_M.start(0)

speedSet = 20

def m_G(speed):
    gpio.output(AIN1, 0)
    gpio.output(AIN2, 1)
    L_M.ChangeDutyCycle(speed)
    gpio.output(BIN1, 0)
    gpio.output(BIN2, 1)
    R_M.ChangeDutyCycle(speed)
    
def m_L(speed):
    gpio.output(AIN1, 1)
    gpio.output(AIN2, 0)
    L_M.ChangeDutyCycle(speed)
    gpio.output(BIN1, 0)
    gpio.output(BIN2, 1)
    R_M.ChangeDutyCycle(speed)

def m_R(speed):
    gpio.output(AIN1, 0)
    gpio.output(AIN2, 1)
    L_M.ChangeDutyCycle(speed)
    gpio.output(BIN1, 1)
    gpio.output(BIN2, 0)
    R_M.ChangeDutyCycle(speed)
    
def m_B(speed):
    gpio.output(AIN1, 1)
    gpio.output(AIN2, 0)
    L_M.ChangeDutyCycle(speed)
    gpio.output(BIN1, 1)
    gpio.output(BIN2, 0)
    R_M.ChangeDutyCycle(speed)
    
def m_Stop():
    gpio.output(AIN1, 0)
    gpio.output(AIN2, 1)
    L_M.ChangeDutyCycle(0)
    gpio.output(BIN1, 0)
    gpio.output(BIN2, 1)
    R_M.ChangeDutyCycle(0)

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
    model_path = "/home/pi/AIAutomachine/lane_navogation_final1.h5"
    model = load_model(model_path)
    
    carState = "stop"
    
    while(cam.isOpened()):
        keyValue = cv2.waitKey(1)
        
        if keyValue == ord('q'):
           break
        elif keyValue == 82:
           print("go")
           carState = "go"
        elif keyValue == 84:
           print("stop")
           carState = "stop"
           
        _, image = cam.read()
        image = cv2.flip(image, -1)
        cv2.imshow('Original', image)
        
        preprocessed = img_preprocess(image)
        cv2.imshow('pre', preprocessed)
        
        X = np.asarray([preprocessed])
        steering_angle = int(model.predict(X)[0])
        print("predict angle : ", steering_angle)
        
        if carState == "go":
           if steering_angle >= 85 and steering_angle <= 95:
              print('go')
              m_G(speedSet)
           elif steering_angle > 96 :
              print('right')
              m_R(speedSet)
           elif steering_angle < 84 :
              print('left')
              m_L(speedSet)
        elif carState == "stop":
           m_Stop()
        
    cv2.destroyAllWindows()
    
    
if __name__ == '__main__':
   main()
   gpio.cleanup()
</code>
</pre>

> 결과화면                    
> 

실제로 주행하였을 시, [실험기록]()에서 2개의 케이스를 가지고 실험하였는 데, 그래프와 확률상으로도 유의미한 결과를 보여주었던 Case1과 Case2가             
서로 상반된 결과가 나왔다.


   









