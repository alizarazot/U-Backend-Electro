from urllib.request import urlopen
from datetime import datetime
from shutil import copyfileobj

import os
from os import path


def save_image(url, dir, name=None) -> str:
    """
    Descarga la última imagen en vivo de la cámara.
    Retorna la ruta de la imagen guardada.
    """

    if name is None:
        name = datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".jpg"

    filepath = path.join(dir, name)

    with urlopen(url) as in_stream, open(filepath, "wb") as out_file:
        copyfileobj(in_stream, out_file)

    return filepath
