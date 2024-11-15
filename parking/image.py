from urllib import request
from datetime import datetime

import os
from os import path

PLATES_DIR = os.getenv("PLATES_DIR")

if PLATES_DIR is None:
    PLATES_DIR = path.abspath(path.join(path.dirname(__file__), "..", "data", "plates"))


def save_live(server_url="http://localhost/capture") -> str:
    """
    Descarga la última imagen en vivo de la cámara.
    Retorna la ruta de la imagen guardada.
    """

    filepath = path.join(PLATES_DIR, datetime.now().strftime("%Y-%m-%d-%H-%M"))
    request.urlretrieve(server_url, filepath)
    return filepath
