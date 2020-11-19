import bluetooth
import subprocess
from multiprocessing import Event
from pubsub import pub, utils
from pubsub import utils as pubsubutils

import logging

import threading


class Bluetooth():
    
    def __init__(self, address, name="HC-05", passkey="1234", port=1):
        """
        address: hexadecimal address in string
        name: BT device display name - string
        passkey: string
        port: integer
        """
        self.address = address
        self.name = name
        self.passkey = passkey
        self.port = port
        self.socket = None
        self.socket_in_use = Event()
        self.socket_in_use.set()

        self.string_buffer = ''

    def connect(self):
        logging.info("Kill other bt-agent processes.")
        subprocess.call("kill -9 `pidof bt-agent`",shell=True)
        logging.info("Set passkey for BT agent.")
        status = subprocess.call("bt-agent " + self.passkey + " &",shell=True)
        try:
            self.socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            self.socket.connect((self.address,self.port))
        except bluetooth.btcommon.BluetoothError as err:
            logging.error('BT Connection error!')
            raise err

    def send(self, msg, echo=False, max_msg_len=128):
        """
        Args:
            - msg: string message
            - echo: wait for echo? boolean
            - max_msg_len: integer - max message lenght to send 
            (n receive on echo if present)
        Returns:
            - None if echo is False - otherwise it will be
            blocked on echo msg and it will return that.
        Raises:
            - AssertionError if msg is longer than limit.
        """
        assert len(msg) <= max_msg_len, "Message is to long"
        self.socket_in_use.wait()
        self.socket_in_use.clear()
        self.socket.send(msg)
        self.socket_in_use.set()
        if echo:
            echo_msg = self.socket.recv(max_msg_len)
            return echo_msg
        else:
            return None

    def receive(self, size=1024, process_msg=False):
        msg = None
        while msg == None:
            self.socket_in_use.wait()
            self.socket_in_use.clear()
            msg = self.socket.recv(size)

            msg = str(msg, 'utf-8')
            if process_msg:
                msg = self.process_raw_message(msg)
            self.socket_in_use.set()
        
        return msg

    def close(self):
        self.socket.close()

    def process_raw_message(self, msg):
        self.string_buffer += msg
        rec_start = self.string_buffer.find('[')
        if rec_start != -1:
            self.string_buffer = self.string_buffer[(rec_start+1):]
        rec_end = self.string_buffer.find(']')
        if rec_end != -1:
            frame = self.string_buffer[:rec_end]
            self.string_buffer = self.string_buffer[rec_end+1:]
            return frame
        
        return None


class BluetoothBroker():
    ALL_TOPICS = pub.ALL_TOPICS
    AUTO_TOPIC = pub.AUTO_TOPIC

    def __init__(self, bt_connection):
        self.bt_connection = bt_connection
        self.publisher = pub
        self.running = False

    def subscribe(self, topic, handler):
        logging.info("Subscribed to {}, with handler {}.".format(topic, handler))
        pub.subscribe(handler, topic)

    def start(self):
        def recv():
            self.running = True
            while self.running:
                frame = self.bt_connection.receive(30, process_msg=True)
                topic, msg = frame.split(':')
                pub.sendMessage(topic, message=msg)

        t = threading.Thread(target=recv,name='bt')
        t.daemon = True
        t.start()

    def stop(self):
        logging.info("Stopping pubsub broker!")
        self.running=False