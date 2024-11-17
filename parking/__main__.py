import os

from os import path
from urllib.error import URLError

from flask import Flask, render_template, send_file

from . import image
from . import plate

# Variables de entorno.
# TODO: Añadirlo como plantilla en el HTML.
CAPTURE_URL = os.getenv("CAPTURE_URL") or "http://192.168.0.110/capture"
PLATES_DIR = os.getenv("PLATES_DIR") or path.abspath(
    path.join(path.dirname(__file__), "data", "plates")
)


app = Flask(__name__)


# Página principal.
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/live")
def live_endpoint():
    path = image.save_image(CAPTURE_URL, PLATES_DIR, "live.jpg")
    return send_file(path, max_age=0)


# Punto de entrada para reconocimiento de placa.
@app.route("/plate")
def plate_endpoint():
    return plate.scan(image.save_image(CAPTURE_URL, PLATES_DIR))


if __name__ == "__main__":
    app.run(host="localhost", port=8000)
