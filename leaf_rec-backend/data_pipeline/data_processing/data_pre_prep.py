from cv2 import imread
import os
from imghdr import what

def pre_prep_data(file):
    print('file', file)
    image_exts = ['jpeg','jpg', 'bmp', 'png']
    
    try: 
        img = imread(file)
        tip = what(file)
        print(img)
        if tip not in image_exts: 
            print('Image not in ext list {}'.format(file))
            os.remove(file)
    except Exception as e: 
        print('Issue with image {}'.format(file))