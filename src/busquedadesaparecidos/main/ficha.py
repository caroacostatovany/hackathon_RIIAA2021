
import nltk
nltk.download('stopwords')
nltk.download('punkt')

# Generic Libraries
from PIL import Image

#Warnings
import warnings
warnings.filterwarnings("ignore")

import cv2
import pytesseract
import numpy as np

from busquedadesaparecidos.utils.limpieza_texto import convierte_minusculas, quitar_caracteres_especiales, quitar_nonascii, quitar_stopwords
from busquedadesaparecidos.ocr.procesamiento_imagen import escala_grises, eliminar_ruido
from busquedadesaparecidos.binarize import binarize
#from nltk.corpus import stopwords
#from nltk.tokenize import word_tokenizer

import tensorflow as tf
import subprocess
import os
import matplotlib.pyplot as plt


class Ficha:
    def __init__(self, path):
        self.path = os.path.abspath(path)
        self.img = cv2.imread(path)
        self.imagen_limpia = self.img
        #self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        self.height, self.width, self.channel = self.img.shape

        #self.text_extraido = pytesseract.image_to_string(self.imagen_limpia)
        self.texto_limpio = ""

    def limpiar_imagen(self):
        gray_img = escala_grises(self.img)
        img_elim_ruido = eliminar_ruido(gray_img)
        imagen_limpia = Image.fromarray(img_elim_ruido)
        imagen_limpia.save('tmp/out_test.JPG')
        #bashCommand = '/home/usr/.pyenv/versions/hackathon/bin/python3.7 ../src/busquedadesaparecidos/binarize/binarize.py -imgpath ./tmp/out_test.JPG -save out_test_2.JPG'

        #process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        #output, error = process.communicate()
        subprocess.call(bashCommand, shell=True)

        img = cv2.imread('out_test_2.JPG')
        kernel = np.ones((2, 2), np.uint8)
        closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
        dilation = cv2.erode(closing, kernel, iterations=1)
        plt.imshow(dilation)
        return dilation


    def limpiar_texto(self):
        #self.texto_limpio = convierte_minusculas(self.text_extraido)
        self.texto_limpio = quitar_caracteres_especiales(self.text_extraido)
        self.texto_limpio = quitar_nonascii(self.texto_limpio)
        self.texto_limpio = quitar_stopwords(self.texto_limpio)

    def limpiar_texto_minusculas(self):
        # self.texto_limpio = convierte_minusculas(self.text_extraido)
        self.texto_limpio = quitar_caracteres_especiales(self.text_extraido)
        self.texto_limpio = quitar_nonascii(self.texto_limpio)
        self.texto_limpio = quitar_stopwords(self.texto_limpio)
