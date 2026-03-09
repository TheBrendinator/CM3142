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
        data: dict = q.get()
        write(data, does_file_exist)


def write(data: dict, does_file_exist: bool):
    with open("climate_sensor.csv", "a", newline="") as csvfile:
        fields = data.keys()
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        if not does_file_exist:
            writer.writeheader()
            does_file_exist = True
        writer.writerow(data)
