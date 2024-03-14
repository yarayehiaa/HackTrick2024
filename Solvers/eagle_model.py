from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras.models import model_from_json, load_model
from sklearn.model_selection import train_test_split
import sklearn
import itertools
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt

import cv2

with open('Solvers\model_arch.json', 'r') as json_file:
    loaded_model_json = json_file.read()
model = model_from_json(loaded_model_json)


model.load_weights('Solvers\weights.h5')
def predictor(x):
    dict_characters = {0: 'Fake', 1: 'Real'}
    new_image_size=(50, 333)
    x = (x * 255).astype(np.uint8)
    x = np.array([cv2.resize(img, new_image_size) for img in x])
    
    a= np.expand_dims(x, axis=-1)
    input= np.repeat(a, 3, axis=-1)
    res=model.predict(input)
    if res[0][0]>0:
        return 1
    else:
        return 0
   





