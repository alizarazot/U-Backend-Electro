from datetime import datetime

from . import ocr


class Plate:
    COST_HOUR = 1_000

    def __init__(self, plate_img):
        self.plate = ocr.scan_plate(plate_img)[:7]
        self.time_in = datetime.now()
        self.time_out = None


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
    }
