import data_gatherer
import data_writer
from multiprocessing import Process, Queue

if __name__ == "__main__":
    # data_gatherer.enable_logging()
    # data_writer.enable_logging()

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
