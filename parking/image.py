from urllib.request import urlopen
from datetime import datetime
from shutil import copyfileobj

import os
from os import path


def save_image(url, dir) -> str:
    """
    Descarga la última imagen en vivo de la cámara.
    Retorna la ruta de la imagen guardada.
    """

    filepath = path.join(dir, datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".jpg")

    with urlopen(url) as in_stream, open(filepath, "wb") as out_file:
        copyfileobj(in_stream, out_file)

    return filepath
