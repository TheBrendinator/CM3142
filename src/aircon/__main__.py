import data_gatherer
import data_writer
from multiprocessing import Process, Queue
import logging.config
from lib import config


# i have no idea why this works but basically after this import, any other
# module this file uses follows the same config
logging.config.dictConfig(config.get_log_config())


if __name__ == "__main__":
    # opting to keep these separate, no reason but it feels right enough
    gather_data = Queue()
    send_data = Queue()

    processor = Process(
        name="DataProcessor",
        target=data_gatherer.main,
        args=(gather_data,),
    )

    receiver = Process(
        name="DataReceiver",
        target=data_writer.main,
        args=(send_data,),
    )

    processor.start()
    receiver.start()

    try:
        while True:
            # this is done here in the event any other components get added that require sending data multiple times
            data = gather_data.get()
            send_data.put(data)

    except KeyboardInterrupt:
        processor.kill()
        receiver.kill()
