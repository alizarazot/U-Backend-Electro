from datetime import datetime
from os import path
import os

import pdfkit

from . import ocr


class Plate:
    COST_HOUR = 14_000

    def __init__(self, plate_img, rotate=False):
        self.plate = ocr.scan_plate(plate_img, rotate)[:7]
        self.time_in = datetime.now()
        self.time_out = None
        self.pdf = None

    def get_price(self):
        cost_second = self.COST_HOUR / 60 / 60

        start = self.time_in
        end = self.time_out
        if end is None:
            end = datetime.now()

        return round((end - start).total_seconds() * cost_second)

    def end_parking(self):
        self.time_out = datetime.now()

    def render_pdf(self, html, data_dir):
        self.pdf = (
            f"{int(self.time_in.timestamp()*1000)}-{self.plate.replace(' ', '-')}.pdf"
        )

        filepath = path.join(data_dir, "pdf", self.pdf)
        os.makedirs(path.dirname(filepath), exist_ok=True)
        pdfkit.from_string(html, filepath)


def encode_json(obj):
    if not isinstance(obj, Plate):
        raise TypeError(f"Cannot serialize object of {type(obj)}")

    time_out = None
    if obj.time_out is not None:
        time_out = obj.time_out.timestamp()

    return {
        "plate": obj.plate,
        "time_in": obj.time_in.timestamp(),
        "time_out": time_out,
        "price": obj.get_price(),
        "pdf": obj.pdf,
    }
