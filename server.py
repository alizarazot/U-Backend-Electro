#!/usr/bin/env python3

import os
from urllib.error import URLError

from flask import Flask

from parking import image

# Variables de entorno.
CAPTURE_URL = os.getenv("CAPTURE_URL")
if CAPTURE_URL is None:
    CAPTURE_URL = "http://192.168.0.110/capture"

app = Flask(__name__)


@app.route("/")
def hello_world():
    try:
        path = image.save_live(CAPTURE_URL)
    except URLError as e:
        return f"<p>Ocurrió un error al descargar la imagen: {e}"

    return f"<p>La ruta es: {path}</p>"
