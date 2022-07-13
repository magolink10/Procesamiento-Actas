#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import easyocr

class Modulo3:
    def ocr(self,imagen,reader):
        texto=reader.readtext(imagen)
        return texto


# In[ ]:




