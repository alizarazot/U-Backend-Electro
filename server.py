import os

from os import path
from urllib.error import URLError

from flask import Flask, send_file

from parking import image
from parking import plate

# Variables de entorno.
CAPTURE_URL = os.getenv("CAPTURE_URL") or "http://192.168.0.110/capture"
PLATES_DIR = os.getenv("PLATES_DIR") or path.abspath(
    path.join(path.dirname(__file__), "data", "plates")
)


app = Flask(__name__)


# Página principal.
@app.route("/")
def home():
    return send_file("frontend/index.html")


# Punto de entrada para reconocimiento de placa.
@app.route("/plate")
def plate_endpoint():
    return plate.scan(image.save_image(CAPTURE_URL, PLATES_DIR))


# Recursos estáticos.


@app.route("/style.css")
def static_style():
    return send_file("frontend/style.css")


@app.route("/script.js")
def static_script():
    return send_file("frontend/script.js")
