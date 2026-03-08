from src.lib.data_types import ClimateData
import csv
from pathlib import Path
from multiprocessing import Queue
import logging

__logging_enabled: bool = False
__file_exist: bool = False


def enable_logging():
    __logging_enabled = True


def main(q: Queue):
    print("Receiver Started")

    if not Path("climate_sensor.csv").exists():
        __does_file_exist = True

    while True:
        data: ClimateData = q.get()
        write(data)
        if __logging_enabled:
            logging.debug(data)
            logging.debug("Data Received")


def write(data: ClimateData):
    with open("climate_sensor.csv", "a", newline="") as csvfile:
        fields = ["timestamp", "humidity", "temperature"]
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        if not __file_exist:
            writer.writeheader()
        writer.writerow(data)
