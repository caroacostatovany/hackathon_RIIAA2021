import cv2
import numpy as np


# Imagen en escala de grises
def escala_grises(imagen):
    return cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)


# Filtro para eliminar ruido
def eliminar_ruido(imagen):
    return cv2.medianBlur(imagen, 5)  # kernel de 5x5


# Binarización de la imagen
def binarizacion(imagen):
    return cv2.threshold(imagen, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


# Operación de dilatación
def dilatacion(imagen):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.dilate(imagen, kernel, iterations=1)


# Operación de erosión
def erosion(imagen):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.erode(imagen, kernel, iterations=1)


# Método de apertura (erosión + dilatación)
def apertura(imagen):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.morphologyEx(imagen, cv2.MORPH_OPEN, kernel)
