import os
import tensorflow as tf

import numpy as np
# from matplotlib import pyplot as plt
from cv2 import imdecode, IMREAD_COLOR 

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten

from tensorflow.keras.metrics import Precision, Recall, BinaryAccuracy
from keras.utils import to_categorical, load_img, img_to_array

from keras.optimizers import RMSprop

from .data_pre_prep import pre_prep_data

def train_model(file):
    # Define relative path from the current notebook location to the data_set directory
    dataset_path = os.path.join('data_set')

    # Get the full absolute path to the data_set directory
    full_path = os.path.abspath(dataset_path)

    # List the directories in the data_set directory
    directories = os.listdir(full_path)
    
    pre_prep_data(full_path)
    
    data = tf.keras.utils.image_dataset_from_directory(dataset_path, labels='inferred')
    data_iterator = data.as_numpy_iterator()

    batch = data_iterator.next()
    
    print('Length of batch',len(batch))
    print('Shape of batch', batch[0].shape)
    print('First element of batch',batch[1])

    print('Max element of batch',batch[0].max())
    
    data = data.map(lambda x,y: (x/255, y))
    data.as_numpy_iterator().next()[0].max()
    

    train_size = int(len(data)*.7)
    val_size = int(len(data)*.2)+1
    test_size = int(len(data)*.1)+1

    train_size+val_size+test_size

    train = data.take(train_size)
    val = data.skip(train_size).take(val_size)
    test = data.skip(train_size+val_size).take(test_size)

    
    model = tf.keras.models.Sequential([
        Conv2D(16, (3,3), 1, activation='relu', input_shape=(256,256,3)),
        MaxPooling2D(),
        Conv2D(32, (3,3), 1, activation='relu'),
        MaxPooling2D(),
        Conv2D(16, (3,3), 1, activation='relu'),
        MaxPooling2D(),
        Flatten(),
        Dense(256, activation='relu'),
        Dense(8, activation='softmax')
    ])
    
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'], run_eagerly=True)
    
    logdir='logs'
    tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=logdir)
    
    train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)
    train_data = train_datagen.flow_from_directory(full_path, target_size=(256, 256), batch_size=32, class_mode='sparse')

    hist = model.fit(train_data, epochs=8, validation_data=val, callbacks=[tensorboard_callback])
        
    pre = Precision()
    re = Recall()
    acc = BinaryAccuracy()

    for batch in test.as_numpy_iterator():
        x, y = batch
        y = to_categorical(y, num_classes=8)
        yhat = model.predict(x)
        pre.update_state(y, yhat)
        re.update_state(y, yhat)
        acc.update_state(y, yhat)

    print (f'Precision:{pre.result().numpy()}, Recall:{re.result().numpy()}, Accuracy:{acc.result().numpy()}')
    

    file_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
    img = imdecode(file_bytes, IMREAD_COLOR)

    resize = tf.image.resize(img, (256,256))

    yhat = model.predict(np.expand_dims(resize/255, 0))
    class_names = ['Balloon vine', 'Coriander', 'Karanda', 'Lemon', 'Mint', 'Mustard', 'Not a matching herb','Oleander', 'Pomegranate']
    
    # probabilities = model.predict(resize)
    image_array = img_to_array(resize)
    image = np.reshape(image_array,[1,256,256,3])
    
    # Get the predicted output probabilities for the input image
    output_probabilities = model.predict(image)
    # Get the index of the maximum value in the output array
    predicted_class_index = np.argmax(output_probabilities)
    # Get the name of the predicted class
    predicted_class_name = class_names[predicted_class_index]
    # Print the predicted class name
    return predicted_class_name
