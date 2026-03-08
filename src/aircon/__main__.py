import data_gatherer
import data_writer
import controller
from multiprocessing import Process, Queue
from lib.data_types import ClimateData
import logging.config
from lib import config


# i have no idea why this works but basically after this import, any other
# module this file uses follows the same config
logging.config.dictConfig(config.get_log_config())


if __name__ == "__main__":
    # opting to keep these separate, no reason but it feels right enough
    gather_queue = Queue()
    writer_queue = Queue()
    controller_queue = Queue()

    processor = Process(
        name="DataProcessor",
        target=data_gatherer.main,
        args=(gather_queue,),
    )

    writer = Process(
        name="DataReceiver",
        target=data_writer.main,
        args=(writer_queue,),
    )

    controller = Process(
        name="AirController",
        target=controller.main,
        args=(controller_queue,),
    )

    processor.start()
    writer.start()

    try:
        while True:
            # TODO: make it run in parallel or whateva
            data: ClimateData = gather_queue.get()
            writer_queue.put(data)
            controller_queue.put(data)

    except KeyboardInterrupt:
        processor.kill()
        writer.kill()
