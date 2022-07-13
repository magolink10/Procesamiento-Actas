#!/usr/bin/env python
# coding: utf-8

# In[2]:


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

class Modulo2:
    #funcion para graficar un número n de imágenes
    def img_comparacion(self,list_img, list_title, list_cmap, size):
      fig, ax = plt.subplots(1,len(list_img), figsize=size)
      for i in range(len(list_img)):
        ax[i].imshow(list_img[i], cmap = list_cmap[i])
        ax[i].set_title(list_title[i])
      plt.show()


    #funcion binarizado
    def binarizado(self,img):
      ret, binary = cv2.threshold(img,240,255,cv2.THRESH_BINARY)
      return np.uint8(binary)


    #procesa la imagen y detecta contornos
    def contornos (self,nueva,num,valor,nombre):
            numero=nueva[0:nueva.shape[1], 940+80*num:1020+80*num]

            numero= cv2.copyMakeBorder(numero,50,0,0,0,cv2.BORDER_CONSTANT,value=[255,255,255])
            up_width = 28
            up_height = 28

            #numero = cv2.resize(numero, (up_width, up_height), interpolation= cv2.INTER_LINEAR)
            numero=self.binarizado(numero)

            contours, _= cv2.findContours(numero, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
            contours_=[]
            yi=0
            yf=120

            for a in contours:
                #print (a)
                x,y,w,h = cv2.boundingRect(a)
                #se prueban varios valores de area antes de llegar a los valores propuestos
                #print (cv2.contourArea(a))

                if(cv2.contourArea(a)>50):
                        contours_.append(a)
                        if(y>yi):
                            yi=y
                        if(y+h<yf):
                            yf=y+h
            h=yf-yi
            temp=int((80-h)/2)
            temp1=80-h-temp
            numero=numero[yi-temp1:yf+temp, 0:numero.shape[1]]
            numero = cv2.resize(numero, (up_width, up_height), interpolation= cv2.INTER_LINEAR)
            return numero

    def identificarActaValida(self,image,reader):
        valida=True
        
        result=reader.readtext(image[250:350, 0:image.shape[1]])

        for a in result:

            if('FIRMAS' in a[1] or 'DE' in a[1] or 'LOS' in a[1] or 'JUNTA' in a[1] or 'RECEPTORA' in a[1] or 'VOTO' in a[1]):
                valida=False
        return valida

    

