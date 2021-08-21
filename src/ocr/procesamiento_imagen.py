# Generic Libraries
from PIL import Image

#Warnings
import warnings
warnings.filterwarnings("ignore")

import cv2
import pytesseract

from src.utils.limpieza_texto import convierte_minusculas, quitar_caracteres_especiales, quitar_nonascii, quitar_stopwords

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('stopwords')
nltk.download('punkt')

# Leemos imagen
path = "../datos/Fichas_manual/Ficheros_Represores_Lopez_Figueroa_Victorico_IMG_6646.JPG"


class Ficha:
    def __init__(self, path):
        self.img = cv2.imread(path)
        self.img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.height, self.width, self.channel = self.img.shape

        self.text_extraido = pytesseract.image_to_string(self.img)
        self.texto_limpio = ""

    def limpiar_texto(self):
        self.texto_limpio = convierte_minusculas(self.text_extraido)
        self.texto_limpio = quitar_caracteres_especiales(self.texto_limpio)
        self.texto_limpio = quitar_nonascii(self.texto_limpio)
        self.texto_limpio = quitar_stopwords(self.texto_limpio)