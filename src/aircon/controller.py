from multiprocessing import Queue
from lib.data_types import ClimateData
import logging


def main(q: Queue):
    # theoretical example of how it would be used
    aircon: bool = False

    while True:
        data: ClimateData = q.get()
        temperature = data["temperature"]
        humidity = data["humidity"]

        if temperature > 23 or (humidity > 50 and temperature > 18):
            aircon = True
            logging.debug(f"aircon: {aircon}")
