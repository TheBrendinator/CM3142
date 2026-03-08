from lib.data_types import ClimateData
import csv
from pathlib import Path
from multiprocessing import Queue
import logging


def main(q: Queue):
    logging.debug("Receiver Started")

    does_file_exist: bool = False

    while True:
        if Path("climate_sensor.csv").exists():
            does_file_exist = True
        else:
            does_file_exist = False
        data: ClimateData = q.get()
        write(data, does_file_exist)
        logging.debug(data)
        logging.debug("Data Received")


def write(data: ClimateData, does_file_exist: bool):
    with open("climate_sensor.csv", "a", newline="") as csvfile:
        fields = ["time", "humidity", "temperature"]
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        if not does_file_exist:
            writer.writeheader()
            does_file_exist = True
        writer.writerow(data)
