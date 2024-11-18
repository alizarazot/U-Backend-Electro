from datetime import datetime

from . import ocr


class Plate:
    COST_HOUR = 7_000

    def __init__(self, plate_img):
        self.plate = ocr.scan_plate(plate_img)[:7]
        self.time_in = datetime.now()
        self.time_out = None

    def get_price(self):
        cost_second = self.COST_HOUR / 60 / 60

        start = self.time_in
        end = self.time_out
        if end is None:
            end = datetime.now()

        return round((end - start).total_seconds() * cost_second)


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
    }
