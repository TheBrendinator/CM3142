from sense_emu import SenseHat
from multiprocessing import Process, Lock, Queue
from time import sleep


class data:
    def __init__(self, humidity, temperature):
        self.__humidity: float = humidity
        self.__temperature: float = temperature
        self.__listHumidity: list[float] = [humidity]
        self.__listTemperature: list[float] = [temperature]
        self.__maxListSize: int = 100

    def max_list_size(self):
        return self.__maxListSize

    def get_dict(self):
        return {"humidity": self.__humidity, "temperature": self.__temperature}

    def record(self, sense_hat: SenseHat):
        # TODO: add a check to see if the value is abnormal
        self.__listHumidity.append(sense_hat.humidity)
        self.__listTemperature.append(sense_hat.temperature)

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
        self.__temperature = self.__get_average(self.__listTemperature)
        self.__humidity = self.__get_average(self.__listHumidity)


def data_gathering_loop():
    print("Gather thread started")
    global cl

    # opting to keep these separate, no reason but it feels right enough
    sense = SenseHat()
    cl = data(sense.humidity, sense.temperature)

    # records x amount of values before initiating the actual loop
    for _ in range(cl.max_list_size()):
        cl.record(sense)

    # gets the first round of averages to have a more up to date value before starting the main part of the code
    cl.get_averages()

    while True:
        # prevent overloading cpu
        sleep(0.01)

        # get data
        cl.record(sense)
        cl.get_averages()


if __name__ == "__main__":
    gatherer = Process(target=data_gathering_loop, args=())
    gatherer.start()
    try:
        gatherer.join()
    finally:
        gatherer.kill()
