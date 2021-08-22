import cv2
import numpy as np

import numpy as np
from skimage.transform import hough_line, hough_line_peaks
from skimage.transform import rotate
from skimage.feature import canny
from skimage.io import imread
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
from scipy.stats import mode


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


def skew_angle_hough_transform(image):
    # convert to edges
    edges = canny(image)
    # Classic straight-line Hough transform between 0.1 - 180 degrees.
    tested_angles = np.deg2rad(np.arange(0.1, 180.0))
    h, theta, d = hough_line(edges, theta=tested_angles)

    # find line peaks and angles
    accum, angles, dists = hough_line_peaks(h, theta, d)

    # round the angles to 2 decimal places and find the most common angle.
    most_common_angle = mode(np.around(angles, decimals=2))[0]

    # convert the angle to degree for rotation.
    skew_angle = np.rad2deg(most_common_angle - np.pi / 2)
    print(skew_angle)
    return skew_angle



