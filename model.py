# -*- coding: utf-8 -*-
"""Model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LyxOdykT8bKuILFBSRbR0M8jMWIbZhu-
"""

Install dependancies and setup
"""

!pip install tensorflow tensorflow-gpu opencv-python matplotlib

from torchvision import datasets, transforms, models

!pip list

import tensorflow as tf
import os

# Avoid OOM errors by setting GPU Memory Consumption Growth
gpus = tf.config.experimental.list_physical_devices('GPU')
for gpu in gpus: 
    tf.config.experimental.set_memory_growth(gpu, True)

tf.config.list_physical_devices('GPU')

"""Remove Dodgy Images"""

import cv2
import imghdr

from google.colab import drive
drive.mount('/content/drive')

dataset_path = '/content/drive/My Drive/dataset/Database'

image_exts = ['jpeg','jpg', 'bmp', 'png']

transform = transforms.Compose([transforms.Resize(255), transforms.CenterCrop(244), transforms.ToTensor()])

dataset = datasets.ImageFolder(dataset_path, transform = transform)

for image_class in os.listdir(dataset_path): 
    for image in os.listdir(os.path.join(dataset_path, image_class)):
        image_path = os.path.join(dataset_path, image_class, image)
        try: 
            img = cv2.imread(image_path)
            tip = imghdr.what(image_path)
            if tip not in image_exts: 
                print('Image not in ext list {}'.format(image_path))
                os.remove(image_path)
        except Exception as e: 
            print('Issue with image {}'.format(image_path))

"""Load Data"""

import numpy as np
from matplotlib import pyplot as plt

data = tf.keras.utils.image_dataset_from_directory('/content/drive/My Drive/dataset/Database')

data_iterator = data.as_numpy_iterator()

batch = data_iterator.next()

fig, ax = plt.subplots(ncols=4, figsize=(20,20))
for idx, img in enumerate(batch[0][:4]):
    ax[idx].imshow(img.astype(int))
    ax[idx].title.set_text(batch[1][idx])

"""Scale Data"""

data = data.map(lambda x,y: (x/255, y))

data.as_numpy_iterator().next()

"""Split Data"""

train_size = int(len(data)*.7)
val_size = int(len(data)*.2)
test_size = int(len(data)*.1)

train_size

train = data.take(train_size)
val = data.skip(train_size).take(val_size)
test = data.skip(train_size+val_size).take(test_size)

"""Build Model"""

train

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout

model = Sequential()

model.add(Conv2D(16, (3,3), 1, activation='relu', input_shape=(256,256,3)))
model.add(MaxPooling2D())
model.add(Conv2D(32, (3,3), 1, activation='relu'))
model.add(MaxPooling2D())
model.add(Conv2D(16, (3,3), 1, activation='relu'))
model.add(MaxPooling2D())
model.add(Flatten())
model.add(Dense(256, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

model.compile('adam', loss=tf.losses.BinaryCrossentropy(), metrics=['accuracy'])

model.summary()

"""Train"""

logdir='logs'

tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=logdir)

hist = model.fit(train, epochs=20, validation_data=val, callbacks=[tensorboard_callback])

"""Plot Performance"""

fig = plt.figure()
plt.plot(hist.history['loss'], color='teal', label='loss')
plt.plot(hist.history['val_loss'], color='orange', label='val_loss')
fig.suptitle('Loss', fontsize=20)
plt.legend(loc="upper left")
plt.show()

fig = plt.figure()
plt.plot(hist.history['accuracy'], color='teal', label='accuracy')
plt.plot(hist.history['val_accuracy'], color='orange', label='val_accuracy')
fig.suptitle('Accuracy', fontsize=20)
plt.legend(loc="upper left")
plt.show()
