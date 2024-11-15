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

import glob
import sys

# Preload OCR model.
ocr_reader = easyocr.Reader(["en", "es"])


def main():
    debug = False
    if len(sys.argv) == 2 and sys.argv[1] == "debug":
        debug = True

    for image in glob.iglob("assets/car*.jpg"):
        get_plate(image, debug)


def get_plate(img_path, debug=False):
    image = cv.imread(img_path)
    if debug:
        show_image("Imagen original", image)

    """
    Paso 1: Simplificar imagen.
    """

    # Convertir a escala de grises.
    image_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    # Reducir ruido.
    image_gray = cv.bilateralFilter(image_gray, 11, 17, 17)
    # show_image('Imagen en escala de grises', image_gray)

    # Extraer bordes de la imagen.
    image_edged = cv.Canny(image_gray, 30, 200)
    # show_image('Bordes de la imagen', image_edged)

    """
    Paso 2: Buscar la placa.
    """

    # Buscar contornos.
    contours = cv.findContours(image_edged.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    contours = sorted(contours, key=cv.contourArea, reverse=True)

    # Buscar el contorno que se parezca más a un rectángulo (4 lados).
    image_ocr = image
    for contour in contours:
        approx = cv.approxPolyDP(contour, 10, True)
        if is_likely_square(approx):
            image_ocr = crop_square(image, image_gray, contour, debug)
            break
    else:
        print("Placa no detectada, utilizando TODA la imagen.")

    """
    Paso 3: Usar OCR para extraer el texto de la placa.
    """

    plate = ocr_reader.readtext(image_ocr, detail=0)
    plate_text = " ".join(plate)

    # Mostrar la imagen.
    show_image(f"Placa: {plate_text}", image)


def crop_square(image, image_gray, location, debug):
    # Remover todo excepto la placa en la imagen.
    image_mask = np.zeros(
        image_gray.shape, np.uint8
    )  # Imagen negra del mismo tamaño de la original.
    image_cleaned = cv.drawContours(image_mask, [location], 0, 255, -1)
    image_cleaned = cv.bitwise_and(image, image, mask=image_mask)
    if debug:
        show_image("Solo la placa en la imagen", image_cleaned)

    # Crear nueva imagen conteniendo solamente la placa.
    x, y = np.where(image_mask == 255)  # Coordenadas de las esquinas de la placa.
    x1, y1 = np.min(x), np.min(y)  # Coordenadas superior izquierda de la placa.
    x2, y2 = np.max(x), np.max(y)  # Coordenadas inferior derecha de la placa.
    # Recortar la imagen.
    image_plate = image[x1 : x2 + 1, y1 : y2 + 1]
    if debug:
        show_image("Placa", image_plate)

    return image_plate


def is_likely_square(approx):
    # Un cuadrado tiene exactamente cuatro vértices.
    if len(approx) != 4:
        return False

    # Verificar que las vértices estén en una posición similar a la de un cuadrado.
    # 1----2
    # |    |
    # 3----4
    points = [(int(point[0][0]), int(point[0][1])) for point in approx]

    x1y1, x2y2, x3y3, x4y4 = None, None, None, None

    # Ubicar X1Y1 y X3Y3.
    x_a = min(points, key=lambda t: t[0])
    points.remove(x_a)
    x_b = min(points, key=lambda t: t[0])
    points.remove(x_b)

    if x_a[1] > x_b[1]:
        x1y1 = x_a
        x3y3 = x_b
    else:
        x1y1 = x_b
        x3y3 = x_a

    # Ubicar X2Y2 y X4Y4.
    x2y2 = max(points, key=lambda t: t[1])
    points.remove(x2y2)
    x4y4 = points[0]

    # Si x1y1(x) está más cerca a x2y2(x) que x3y3(x), probablemente no sea un cuadrado.
    if (x2y2[0] - x1y1[0]) < ((x4y4[0] - x3y3[0]) / 2):
        return False
    if (x4y4[0] - x3y3[0]) < ((x2y2[0] - x1y1[0]) / 2):
        return False
    # TODO: Hacer lo mismo en el eje vertical.

    return True


def show_image(title, image, cvt_color=cv.COLOR_BGR2RGB):
    image = cv.cvtColor(image, cvt_color)

    plot.imshow(image)
    plot.title(title)
    plot.show()


if __name__ == "__main__":
    main()
