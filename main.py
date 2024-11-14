#!/usr/bin/env python3

"""
El proceso de reconocimiento de placas requiere de los siguientes pasos:
    1. Simplificar la imagen: Dejarla a blanco y negro y solo dejar los bordes.
    2. Buscar la placa: Bordes rectángulares tienen alta probabilidad de ser la placa.
    3. Aplicar OCR a la placa.
"""

import cv2 as cv
import numpy as np

import imutils
import easyocr

from matplotlib import pyplot as plot

import sys

def main():
    img_path = sys.argv[1]

    image = cv.imread(img_path)
    #show_image('Imagen original', image)

    """
    Paso 1: Simplificar imagen.
    """

    # Convertir a escala de grises.
    image_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    # Reducir ruido.
    image_gray = cv.bilateralFilter(image_gray, 11, 17, 17)
    #show_image('Imagen en escala de grises', image_gray)

    # Extraer bordes de la imagen.
    image_edged = cv.Canny(image_gray, 30, 200)
    #show_image('Bordes de la imagen', image_edged)

    """
    Paso 2: Buscar la placa.
    """

    # Buscar contornos.
    contours = cv.findContours(image_edged.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    # Elegir los 10 mejores contornos.
    contours = sorted(contours, key=cv.contourArea, reverse=True)
    
    # Buscar el contorno que se parezca más a un rectángulo (4 lados).
    location = None
    for contour in contours:
        approx = cv.approxPolyDP(contour, 10, True)
        if len(approx) == 4:
            location = approx
            break
    #print("Ubicación de la placa:", location)

    # Remover todo excepto la placa en la imagen.
    image_mask = np.zeros(image_gray.shape, np.uint8) # Imagen negra del mismo tamaño de la original.
    image_cleaned = cv.drawContours(image_mask, [location], 0, 255, -1)
    image_cleaned = cv.bitwise_and(image, image, mask=image_mask)
    #show_image('Solo la placa en la imagen', image_cleaned)

    # Crear nueva imagen conteniendo solamente la placa.
    x, y = np.where(image_mask == 255) # Coordenadas de las esquinas de la placa.
    x1, y1 = np.min(x), np.min(y) # Coordenadas superior izquierda de la placa.
    x2, y2 = np.max(x), np.max(y) # Coordenadas inferior derecha de la placa.
    # Recortar la imagen.
    image_plate = image_gray[x1:x2+1, y1:y2+1]
    #show_image('Placa', image_plate)

    """
    Paso 3: Usar OCR para extraer el texto de la placa.
    """

    r = easyocr.Reader(['en'])
    plate = r.readtext(image_plate)
    plate = plate[0][1]

    # Mostrar la imagen.
    show_image(f'Placa: {plate}', image)

def show_image(title, image, cvt_color=cv.COLOR_BGR2RGB):
    image = cv.cvtColor(image, cvt_color)

    plot.imshow(image)
    plot.title(title)
    plot.show()

if __name__ == '__main__': main()
