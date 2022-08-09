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
다음 코드를 실행하여 압축을 풀자.   

<code>!unzip -qq "/content/drive/MyDrive/AIAutomachine/Pic.zip"</code>

## 7-3-1.py
<pre>
<code>
import os
import random
import fnmatch
import datetime
import pickle

import numpy as np
np.set_printoptions(formatter={'float_kind' : lambda x: "%.4f" % x})

import pandas as pd
pd.set_option('display.width', 300)
pd.set_option('display.float_format', '{:,.4f}'.format)
pd.set_option('display.max_colwidth', 200)

import tensorflow as tf
import tensorflow.keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPool2D, Dropout, Flatten, Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import load_model

print(f'tf.__version__ : {tf.__version__}' )
print(f'.keras.__version__: {tf.keras.__version__}' ) 

from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split

import cv2 
from imgaug import augmenters as lmg_aug
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
%matplotlib inline
from PIL import Image
</code>
</pre>


이제 압축을 푼 사진을 가져온다.            

## 7-3-2.py
<pre>
<code>
data_dir = '/content/Pic'
file_list = os.listdir(data_dir)
image_paths = []
steering_angles = []
pattern = '*.png'
for filename in file_list:
  if fnmatch.fnmatch(filename, pattern):
    image_paths.append(os.path.join(data_dir, filename))
    angle = int(filename[-7:-4])
    steering_angles.append(angle)

image_index = 20
plt.imshow(Image.open(image_paths[image_index]))
print('image_path : %s' % image_paths[image_index])
print('steering_Angle : %d' % steering_angles[image_index])
df = pd.DataFrame()
df['ImagePath'] = image_paths
df['Angle'] = steering_angles
</code>
</pre>

다음은 조향각의 분포 확인하기다.

## 7-3-3.py
<pre>
<code>
num_of_bins = 25
hist, bins = np.histogram(df['Angle'], num_of_bins)

fig, axes = plt.subplots(1, 1, figsize=(12, 4))
axes.hist(df['Angle'], bins=num_of_bins, width=1, color='blue')
</code>
</pre>

학습 데이터와 검증 데이터를 분리하기 

## 7-3-4.py
<pre>
<code>
X_train, X_valid, y_train, y_valid = train_test_split(image_paths, steering_angles, test_size=0.2)
print('Training data : %d\nValidation data : %d' % (len(X_train), len(y_valid)))

fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].hist(y_train, bins=num_of_bins, width=1, color='blue')
axes[0].set_title('Training Data')
axes[1].hist(y_valid, bins=num_of_bins, width=1, color='red')
axes[1].set_title('Validation Data')
</code>
</pre>

이미지 읽어오기 및 정규화하기

## 7-3-5.py
<pre>
<code>
def my_imread(image_paths):
  image = cv2.imread(image_paths)
  return image

def img_preprocess(image):
  image = image/255
  return image

fig, axes = plt.subplots(1, 2, figsize=(15, 10))
image_orig = my_imread(image_paths[image_index])
image_processed = img_preprocess(image_orig)
axes[0].imshow(image_orig)
axes[0].set_title('orig')
axes[1].imshow(image_processed)
axes[1].set_title('processed')
</code>
</pre>

NVIDIA Model 구성하기

## 7-3-6.py
<pre>
<code>
def nvidia_model():
  model = Sequential(name = 'NVIDIA_Model')
  
  model.add(Conv2D(24, (5, 5), strides=(2, 2), input_shape=(66, 200, 3), activation='elu'))
  model.add(Conv2D(36, (5, 5), strides=(2, 2), activation='elu'))
  model.add(Conv2D(48, (5, 5), strides=(2, 2), activation='elu'))
  model.add(Conv2D(64, (3, 3), activation='elu'))
  model.add(Dropout(0.2))
  model.add(Conv2D(64, (3, 3), activation='elu'))

  model.add(Flatten())
  model.add(Dropout(0.2))
  model.add(Dense(100, activation='elu'))
  model.add(Dense(50, activation='elu'))
  model.add(Dense(10, activation='elu'))

  model.add(Dense(1))

  optimizer = Adam(lr=1e-3)
  model.compile(loss='mse', optimizer=optimizer)

  return model

model = nvidia_model()
print(model.summary())
</code>
</pre>


학습 데이터 생성하기

## 7-3-7.py
<pre>
<code>
from numpy.lib.type_check import asfarray
def image_data_generator(image_paths, steering_angles, batch_size):
  while True:
    batch_images = []
    batch_steering_angles = []

    for i in range(batch_size):
      random_index = random.randint(0, len(image_paths) - 1 )
      image_path = image_paths[random_index]
      image = my_imread(image_paths[random_index])
      steering_angle = steering_angles[random_index]

      image = img_preprocess(image)
      batch_images.append(image)
      batch_steering_angles.append(steering_angle)

    yield( np.asarray(batch_images), np.asarray(batch_steering_angles))


ncol = 2
nrow = 2

X_train_batch, y_train_batch = next(image_data_generator(X_train, y_train, nrow))
X_valid_batch, y_valid_batch = next(image_data_generator(X_valid, y_valid, nrow))

fig, axes = plt.subplots(nrow, ncol, figsize=(15, 6))
fig.tight_layout()

for i in range(nrow):
  axes[i][0].imshow(X_train_batch[i])
  axes[i][0].set_title('Training, angle=%s' % y_train_batch[i])
  axes[i][1].imshow(X_valid_batch[i])
  axes[i][1].set_title('Training, angle=%s' % y_valid_batch[i]) 
</code>
</pre>


모델 학습시키기 (약 20분~30분 정도 소요됨.)

## 7-3-8.py
<pre>
<code>
model_output_dir = "/content/drive/MyDrive/AIAutomachine"

checkpoint_callback = tensorflow.keras.callbacks.ModelCheckpoint(filepath=os.path.join(model_output_dir, 'lane_navigation_check.h5'), verbose=1, save_best_only=True)

history = model.fit_generator(image_data_generator(X_train, y_train, batch_size=100), steps_per_epoch=300, epochs=10, validation_data = image_data_generator(X_valid, y_valid, batch_size=100), validation_steps=200, verbose=1, shuffle=1, callbacks=[checkpoint_callback])

model.save(os.path.join(model_output_dir, 'lane_navogation_final.h5'))

history_path = os.path.join(model_output_dir, 'history.pickle')

with open(history_path, 'wb') as f:
  pickle.dump(history.history, f, pickle.HIGHEST_PROTOCOL)
</code>
</pre>

결과 확인하기

## 7-3-9.py
<pre>
<code>
history.history

history_path = os.path.join(model_output_dir, 'history.pickle')
with open(history_path, 'rb') as f:
  history = pickle.load(f)

history
plt.plot(history['loss'], color='blue')
plt.plot(history['val_loss'], color='red')
plt.legend(['training loss', 'validation loss'])
</code>
</pre>

> 결과화면1                
> (학습을 이상하게 하여 실패)                
> <그림>                    

> 결과화면2                 
> 제대로 된 모습              
> <그림>                  


검증하기

## 7-3-10.py
<pre>
<code>
from sklearn.metrics import mean_squared_error, r2_score

def summarize_prediction(Y_true, Y_pred):

  mse = mean_squared_error(Y_true, Y_pred)
  r_squared = r2_score(Y_true, Y_pred)

  print(f'mse = {mse:2}')
  print(f'r_squared = {r_squared:2%}')
  print()

def predict_and_summarize(X, Y):
  model = load_model(f'{model_output_dir}/lane_navigation_check.h5')
  Y_pred = model.predict(X)
  summarize_prediction(Y, Y_pred)
  return Y_pred

n_tests = 100
X_test, y_test = next(image_data_generator(X_valid, y_valid, 100))

y_pred = predict_and_summarize(X_test, y_test)

n_tests_show = 2
fig, axes = plt.subplots(n_tests_show, 1, figsize=(10, 4 * n_tests_show))
for i in range(n_tests_show):
  axes[i].imshow(X_test[i])
  axes[i].set_title(f'actual angle={y_test[i]}, predicted angle={int(y_pred[i])}, diff = {int(y_pred[i])-y_test[i]}')
</code>
</pre>

> 결과화면 1                 
> 89%  --- 실패함. 다시 학습해야함.                 
> <그림>                

> 결과화면 2                   
> % --- 안정적임.                  
> <그림>                 


-----------------------------------------------------------------------------------------------------------------------

결과화면 1을 봤다시피 실험은 실패했다. 그 이유는 다음 챕터 8에서 확인할 수 있다.                        
결과화면 2는 [Chapter 8]()에서 다시 실시한 실험으로 나온 수치이다.


-----------------------------------------------------------------------------------------------------------------------

##### 여담

import tensorflow.keras 에서 문제가 생기는 데 다음 링크를 타고 보면 문제의 원인을 알 수 있다.

[오류](https://stackoverflow.com/questions/71000250/import-tensorflow-keras-could-not-be-resolved-after-upgrading-to-tensorflow-2)                

실험을 오래 하다보니 [이러한 문제](https://limitsinx.tistory.com/135)가 생겼는 데 찾아보니....                
기다리거나, 돈을 내서 돌리는 수밖에 없다고 한다....






