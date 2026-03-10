import csv
from pathlib import Path
from data_types import DisplayData
import logging


class Writer:
    def __init__(self) -> None:
        self.filename = "data.csv"
        self.data: DisplayData

    def write(self) -> bool:
        # If data is empty, don't write
        if not self.data:
            logging.debug("No data, not writing")
            return False

        does_file_exist: bool = False

        while True:
            if Path("climate_sensor.csv").exists():
                does_file_exist = True
            else:
                does_file_exist = False
            self.__write(self.filename, does_file_exist)

    def __write(self, filename: str, does_file_exist: bool):
        logging.debug("Writing")
        with open(filename, "a", newline="") as csvfile:
            fieldnames: str = ""
            data: str = ""
            for classType in self.data.values():
                fieldnames += classType.__name__ + ","
                for classData in classType.values():
                    data += classData + ","

            fields = self.data.keys()
            writer = csv.writer(csvfile, delimiter="")
            if not does_file_exist:
                writer.writeheader()
                does_file_exist = True
            for type in self.data.keys():
                writer.writerow(type.values())


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
