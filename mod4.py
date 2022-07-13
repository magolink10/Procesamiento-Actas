#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from pyunpack import Archive
import os
import glob
import cv2
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage
from skimage import (io, filters, morphology)
from skimage.color import rgb2gray
from skimage.morphology import erosion, dilation, opening, closing
from skimage.morphology import disk, diamond, ball, cube, octahedron, star
import easyocr
import tensorflow as tf
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
import numpy as np
import math
import uuid
from difflib import SequenceMatcher as SM

class Modulo4:
    
    def predecir(self,imagen,modelo):
        predicted=''
        rep=np.array(255-imagen)
        rep=rep.reshape(1,28, 28, 1)
        rep = rep.astype('float32') / 255
        #print (np.shape(rep))
        pred=modelo.predict(rep)
        predicted = np.argmax(pred, axis=1)  
        return predicted

