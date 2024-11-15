#!/usr/bin/env python3

from urllib.error import URLError

from flask import Flask

from parking import image

app = Flask(__name__)


@app.route("/")
def hello_world():
    try:
        path = image.save_live()
    except URLError as e:
        return f"<p>Ocurrió un error al descargar la imagen: {e}"

    return f"<p>La ruta es: {path}</p>"
