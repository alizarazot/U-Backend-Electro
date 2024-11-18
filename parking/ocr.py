"""
El proceso de reconocimiento de placas requiere de los siguientes pasos:
    1. Simplificar la imagen: Dejarla a blanco y negro y solo dejar los bordes.
    2. Buscar la placa: Bordes rectángulares tienen alta probabilidad de ser la placa.
    3. Aplicar OCR a la placa.
"""

import cv2 as cv

import easyocr

# Preload OCR model.
ocr_reader = easyocr.Reader(["en"], gpu=False)


def scan_plate(img_path) -> str:
    """
    Escanea una imagen y devuelve la placa.

    Si no se encuentra la placa, retorna una cadena vacía.
    """

    image = cv.imread(img_path)
    plate = ocr_reader.readtext(
        image,
        detail=0,
        batch_size=10000,
        allowlist="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ",
    )

    plate_text = ""
    if len(plate) != 0:
        plate_text = " ".join(plate)

    return plate_text