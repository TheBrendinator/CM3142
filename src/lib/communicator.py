import websockets
import socket
import asyncio
import re
import threading
import json
import data_types

# This file is built under the assumption that every device will act as a host

# It runs on 3 separate threads: a server, a client, and a writer

# The server will send whatever data the specific module the pi is running produces using 'send_data()'
# The client will receive all data from the other devices on the network
# Both of them will send data to a writer, which will combine everything and write to storage using data_types


class __Server(threading.Thread):
    def __init__(self, default_port: int):
        # Auto selects device IP address
        # NOTE: Only grabs local device IP Should work fine for our use cases
        self.device_ip: str = socket.gethostbyname(socket.gethostname())

        self.port: int = default_port
        self.local_data: dict = {}
        self.clients: dict = {}
        self._stop_event = threading.Event()

    def start(self):
        asyncio.run(self.__start_server())

    def stop(self):
        self._stop_event.set()

    def stopped(self) -> bool:
        return self._stop_event.is_set()

    def update_local_data(self, local_data):
        self.local_data = local_data

    async def __start_server(self):
        # Allows for clients to disconnect and reconnect at any time
        server = await websockets.serve(
            self.__server_loop,
            self.device_ip,
            self.port,
        )
        await server.wait_closed()

    async def __server_loop(self, websocket):
        # Get signal from each client and send data to them
        self.clients[websocket] = await websocket.recv()
        client = json.loads(self.clients[websocket])
        await websocket.send(json.dumps({"client": client, "data": self.local_data}))

        # Check when to stop
        # if self.stopped():
        # TODO: figure out how to make it stop


class __Client(threading.Thread):
    def __init__(self, default_port: int):
        self.label = "CHANGE THIS"
        self.port: int = default_port
        self._stop_event = threading.Event()

    def set_label(self, newLabel):
        self.label = newLabel

    def start(self):
        asyncio.run(self.__run_client())

    def stop(self):
        self._stop_event.set()

    def stopped(self) -> bool:
        return self._stop_event.is_set()

    async def __run_client(self):
        # TODO: Make this be able to connect to a multitude of devices
        # This might be doable by having it run 'arp -a' and getting all the ip's from there
        # WARNING: IF I DO USE 'arp -a' DO NOT CONNECT TO FULL NETWORK BEFORE RUNNING THIS
        asyncio.run(self.__receiver("127.0.0.1"))

    async def __receiver(self, ip: str):
        # Convert IP to websocket format
        ws = "ws://" + ip + ":" + str(self.port)

        # Connect to device with listed IP
        async with websockets.connect(ws) as websocket:
            # Send ID to server
            await websocket.send(json.dumps({"label": device_label}))

            # Receive Data from server
            response = json.loads(await websocket.recv())

            # Check when to stop
            # if self.stopped():
            # TODO: figure out how to make it stop


# TODO: Make a writer that can pull all the data together and write to a local CSV


def set_device_label(label: str):
    global device_label
    device_label = label


# This should be automatically handled but it's here just in case
def set_device_ip(ip: str):
    # Returns false if the ip is not a valid ip
    # Regex obtained from https://stackoverflow.com/questions/5284147/validating-ipv4-addresses-with-regexp
    if bool(re.search(r"^(((?!25?[6-9])[12]\d|[1-9])?\d\.?\b){4}$", ip)):
        global device_ip
        device_ip = ip
        return True

    return False


default_port: int = 8765

server = __Server(default_port)
client = __Client(default_port)


# Any modules wanting to use this file should just call this function after configuring it properly
def run():
    # Creates a new thread despite running async in case sleep() is used anywhere improperly
    # An unnecessary safety step really
    threading.Thread(name="Server", target=server.start, args=())
    threading.Thread(name="Client", target=client.start, args=())


def stop():
    server.stop()
    client.stop()


def send_data(data: dict):
    server.update_local_data(data)
