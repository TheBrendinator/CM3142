from sense_emu import SenseHat
import logging
import threading
from multiprocessing import Process, Lock, Queue
from typing import TypedDict
from time import sleep
from time import asctime
import csv
from pathlib import Path

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)-8s | process: %(processName)-12s | thread: %(threadName)-4s | %(message)s",
)


class DataDict(TypedDict):
    time: str
    humidity: float
    temperature: float


class DataProcess:
    def __init__(self, humidity, temperature):
        self.__current_time: str = asctime()
        self.__humidity: float = humidity
        self.__temperature: float = temperature
        self.__listHumidity: list[float] = [humidity]
        self.__listTemperature: list[float] = [temperature]
        self.__maxListSize: int = 100
        self.__lock = Lock()

    def max_list_size(self):
        return self.__maxListSize

    def get_dict(self):
        self.__lock.acquire()
        dd = DataDict(
            time=self.__current_time,
            temperature=self.__temperature,
            humidity=self.__humidity,
        )
        self.__lock.release()
        return dd

    def record(self, sense_hat: SenseHat):
        # TODO: add a check to see if the value is abnormal
        humidity = sense_hat.humidity
        temperature = sense_hat.temperature

        self.__listHumidity.append(humidity)
        self.__listTemperature.append(temperature)

        # Limit list size to the last maxListSize values
        # For long term usage you wouldn't want the pi running out of ram
        # Also keeps the average generation quick and up to date
        # TODO: add ability to write erased values to storage
        self.__listTemperature = self.__listTemperature[-self.max_list_size() :]
        self.__listHumidity = self.__listHumidity[-self.max_list_size() :]

    def __get_average(self, list):
        avg: float = 0
        for val in list:
            avg = val
        return avg

    def get_averages(self):
        avgTemp = self.__get_average(self.__listTemperature)
        avgHumid = self.__get_average(self.__listHumidity)

        self.__lock.acquire()
        self.__current_time = asctime()
        self.__temperature = avgTemp
        self.__humidity = avgHumid
        self.__lock.release()


def process_processor(q: Queue):
    sense = SenseHat()
    global cl
    cl = DataProcess(sense.humidity, sense.temperature)

    # records x amount of values before initiating the actual loop
    for _ in range(cl.max_list_size()):
        cl.record(sense)

    # gets the first round of averages to have a more up to date value before starting the main part of the code
    cl.get_averages()

    # This runs as a thread since it pauses until the data is received somewhere
    pusher = threading.Thread(
        target=processor_push_data,
        args=(q,),
    )
    pusher.name = "Pusher"
    pusher.start()

    while True:
        # prevent overloading cpu
        sleep(0.01)

        # get data
        cl.record(sense)
        cl.get_averages()

        # logging.debug("Recording Finished")


def processor_push_data(q: Queue):
    while True:
        sleep(1)
        q.put(cl.get_dict())
        # logging.debug("Data Sent")


def process_receiver(q: Queue):
    print("Receiver Started")
    while True:
        data: DataDict = q.get()
        receiver_write(data)
        # logging.debug(data)
        # logging.debug("Data Received")


def receiver_write(data: DataDict):
    fresh: bool = False

    if not Path("climate_sensor.csv").exists():
        fresh = True

    with open("climate_sensor.csv", "a", newline="") as csvfile:
        fields = ["timestamp", "humidity", "temperature"]
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        if fresh:
            writer.writeheader()
        writer.writerow(
            {
                "timestamp": asctime(),
                "humidity": data["humidity"],
                "temperature": data["temperature"],
            }
        )


if __name__ == "__main__":
    # opting to keep these separate, no reason but it feels right enough
    queue = Queue()

    processor = Process(
        target=process_processor,
        args=(queue,),
    )
    processor.name = "DataProcessor"
    receiver = Process(
        target=process_receiver,
        args=(queue,),
    )
    receiver.name = "DataReceiver"
    processor.start()
    receiver.start()
    try:
        processor.join()
        receiver.join()
    except KeyboardInterrupt:
        processor.kill()
        receiver.kill()
