from lib.data_types import ClimateData
import logging
from sense_emu import SenseHat
import threading
from multiprocessing import Lock, Queue
from time import asctime, sleep


class __ClimateDataProcesser:
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
        dd: ClimateData = {
            "time_recorded":self.__current_time,
            "temperature":self.__temperature,
            "humidity":self.__humidity
        }
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
        # Also keeps the generation of averages quick and up to date
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


def main(q: Queue):
    sense = SenseHat()
    global cl
    cl = __ClimateDataProcesser(sense.humidity, sense.temperature)

    # records x amount of values before initiating the actual loop
    for _ in range(cl.max_list_size()):
        cl.record(sense)

    # gets the first round of averages to have a more up to date value before starting the main part of the code
    cl.get_averages()

    # runs as separate thread to prevent blocking this thread
    pusher = threading.Thread(
        target=__push_data,
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

        logging.debug("Recording Finished")


def __push_data(q: Queue):
    while True:
        sleep(1)
        q.put(cl.get_dict())
        logging.debug("Data Sent")
