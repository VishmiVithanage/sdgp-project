"""Remove Dodgy Images"""
import os
import cv2
import imghdr
import tensorflow as tf

print('----- Start Cleaning Images ----')
dataset_path = '/Users/vikumdabare/Documents/projects/leaf_recognition/leaf_recognition/data_set'

directories = os.listdir(dataset_path)
print(directories)

image_exts = ['jpeg','jpg', 'bmp', 'png']

for image_class in os.listdir(dataset_path):
  print(image_class)

for image_class in os.listdir(dataset_path): 
   
    image_path = os.path.join(dataset_path, image_class)
    try: 
        img = cv2.imread(image_path)
        tip = imghdr.what(image_path)
        if tip not in image_exts: 
            print('Image not in ext list {}'.format(image_path))
            os.remove(image_path)
    except Exception as e: 
        print('Issue with image {}'.format(image_path))

print('---- Start Processing ----')
"""Load Data"""

import numpy as np
from matplotlib import pyplot as plt

data = tf.keras.utils.image_dataset_from_directory(dataset_path)

data_iterator = data.as_numpy_iterator()

batch = data_iterator.next()

len(batch)

batch[0].shape

batch[1]

fig, ax = plt.subplots(ncols=4, figsize=(20,20))
for idx, img in enumerate(batch[0][:4]):
    ax[idx].imshow(img.astype(int))
    ax[idx].title.set_text(batch[1][idx])

batch[0].max()

"""Data Preprocessing
Scale Data/ Normalize
"""

data = data.map(lambda x,y: (x/255, y))

data.as_numpy_iterator().next()[0].max()