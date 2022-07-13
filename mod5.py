#!/usr/bin/env python
# coding: utf-8

# In[5]:


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
from mod2 import Modulo2
from mod3 import Modulo3
from mod4 import Modulo4


class Modulo5:
    def iniciar(self,archivo,cadena,nombre,modelo):
        global numerror
        global numtotal
        error=0
        actavalida=True

        Archive(archivo).extractall("temp/")

        #extraccion imagenes a ser procesadas, se almacenan en la lista images
        images = [cv2.imread(file,0) for file in sorted(glob.glob('temp/*.tif'))]

        for i in images:

            i=modulo2.binarizado(i)
            scale_percent = 50 # 50% del tamaño original para ahorrar procesamiento
            width = int(i.shape[1] * scale_percent / 100)
            height = int(i.shape[0] * scale_percent / 100)
            dim = (width, height)
            resized = cv2.resize(i, dim, interpolation = cv2.INTER_AREA)

            if (modulo2.identificarActaValida(resized,reader)):
                pass
            else:
                continue

            #la imagen puede tener hasta 11 espacios donde puede haber información
            for a in range (0,11):
                nueva=resized[335+118*a:453+118*a, 0:resized.shape[1]]
                #nueva=resized[315+95*a:410+95*a, 0:resized.shape[1]]

                result=modulo3.ocr(nueva[0:resized.shape[1], 150:500],reader)
                x=''
                for res in result:
                    x=x+res[1]+" "

                if (x!='' and 'VOTA' not in x):
                    #print (x.upper())
                    div=''
                    if ('VOT' in x.upper()):
                        for texto in cadena:
                            grado=SM(None, x.upper().split('(')[0], texto.upper().split('(')[0]).ratio()

                            if(grado>0.90):
                                div=texto.split(':')[1].rjust(4, '0')
                                #print (x, div[0],div[1],div[2],grado)
                    else:

                        for texto in cadena:
                            grado=SM(None, x.upper(), texto.upper()).ratio()

                            if(grado>0.70):
                                div=texto.split(':')[1].rjust(4, '0')
                                #print (x,div[0],div[1],div[2])
                    if(div!=''):    
                        numtotal+=1
                        if(1==1):
                            numero1=modulo2.contornos (nueva,0,div[0],nombre)
                            numero2=modulo2.contornos (nueva,1,div[1],nombre)
                            numero3=modulo2.contornos (nueva,2,div[2],nombre)
                            num11=str(modulo4.predecir(numero1,modelo)[0])
                            num12=str(modulo4.predecir(numero1,modelo1)[0])
                            num21=str(modulo4.predecir(numero2,modelo)[0])
                            num22=str(modulo4.predecir(numero2,modelo1)[0])
                            num31=str(modulo4.predecir(numero3,modelo)[0])
                            num32=str(modulo4.predecir(numero3,modelo1)[0])
                            prediccion=num11+num21+num31
                            prediccion1=num12+num22+num32
                            real=str(div[0])+str(div[1])+(div[2])
                            encontrado1=False
                            encontrado2=False
                            encontrado3=False

                            if (str(div[0])==num11 or str(div[0])==num12):
                                encontrado1=True
                            if (str(div[1])==num21 or str(div[1])==num22):
                                encontrado2=True
                            if (str(div[2])==num31 or str(div[2])==num32):
                                encontrado3=True

                            if(encontrado1==True and encontrado2==True and encontrado3==True):
                                pass
                            else:
                                actavalida=False
                                numerror+=1
                                error+=1
                                '''print (x)
                                print('Real: '+real,'Pred1: '+ prediccion,'Pred2: '+ prediccion1)
                                fig, ax = plt.subplots(1,1, figsize=[20, 20])
                                ax.imshow(nueva, cmap = 'gray')
                                plt.show()
                                modulo2.img_comparacion([numero1,numero2,numero3], 
                                          ['numero1','numero2','numero3'], 
                                          ['gray','gray','gray'], 
                                          [5, 5])'''
                                path="Errores/2021/erroresImagen/"+nombre+"-"+str(error)+".jpg"
                                cv2.imwrite(path, nueva)
                                ruta="Errores/2021/erroresInfo/"+nombre+"-"+str(error)+".txt"
                                f = open(ruta, "w")
                                f.write(real+"\n")
                                f.write(prediccion+"\n")
                                f.write(prediccion1+"\n")        
                                f.close() 
        if(actavalida):
            f = open('Errores/2021/validas.txt', "a")
            f.write(nombre+"\n")        
            f.close()




        #Se eliminan los archivos extraidos
        files = glob.glob('temp/*')
        for f in files:
            os.remove(f)




