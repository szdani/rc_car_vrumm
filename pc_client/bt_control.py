import bluetooth
import subprocess
import time

from pynput import keyboard



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

    def connect(self):
        print("Kill other bt-agent processes.")
        subprocess.call("kill -9 `pidof bt-agent`",shell=True)
        print("Set passkey for BT agent.")
        status = subprocess.call("bt-agent " + self.passkey + " &",shell=True)
        try:
            self.socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            self.socket.connect((self.address,self.port))
        except bluetooth.btcommon.BluetoothError as err:
            print('BT Connection error!')
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
        self.socket.send(msg)
        if echo:
            echo_msg = self.socket.recv(max_msg_len)
            return echo_msg
        else:
            return None

    def close(self):
        self.socket.close()


class Controller():
    FORWARD_LEFT = "F_LEFT"
    FORWARD_RIGHT = "F_RIGHT"
    FORWARD = "FORWARD"
    BACK = "BACK"
    BACK_LEFT = "B_LEFT"
    BACK_RIGHT = "B_RIGHT"
    STOP = "STOP"

    def __init__(self, comm=None, verbose=False):
        if comm is not None:
            print('Using {} for communication.'.format(comm))
        self.comm = comm
        self.verbose = verbose
        self.is_forward = False
        self.is_backward = False
        self.is_right = False
        self.is_left = False
        self.state = Controller.STOP
        self.time = None

    def _get_motor_control_message(self):
        if self.is_forward and self.is_backward:
            return Controller.STOP
        elif self.is_right and self.is_left:
            return Controller.STOP
        elif self.is_forward and not (self.is_right or self.is_left):
            return Controller.FORWARD
        elif (self.is_forward and self.is_right) or (not self.is_backward and self.is_right):
            return Controller.FORWARD_RIGHT
        elif (self.is_forward and self.is_left) or (not self.is_backward and self.is_left):
            return Controller.FORWARD_LEFT
        elif (self.is_backward and self.is_right) or (not self.is_forward and self.is_right):
            return Controller.BACK_RIGHT
        elif (self.is_backward and self.is_left) or (not self.is_forward and self.is_left):
            return Controller.BACK_LEFT
        elif self.is_backward:
            return Controller.BACK
        else:
            return Controller.STOP

    def _is_udpate_needed(self, current_time, new_state, delay=0.65):
        flag = False
        if self.time is None or (self.time + delay) <= current_time:
            flag = True
        if new_state != self.state: #new_state is Controller.STOP and
            flag = True
        return flag

    def _send_message(self):
        new_state = self._get_motor_control_message()
        if new_state is None:
            return
        
        current_time = time.time()
        if self._is_udpate_needed(current_time, new_state):
            self.comm.send(new_state)
            time.sleep(0.2)
            self.time = current_time
            if self.verbose:
                print("\n{}->{}".format(self.state, new_state))
        self.state = new_state

    def on_press(self, key):
        if key == keyboard.Key.left:
            self.is_left = True
        elif key == keyboard.Key.right:
            self.is_right = True
        elif key == keyboard.Key.up:
            self.is_forward = True
        elif key == keyboard.Key.down:
            self.is_backward = True
        
        self._send_message()

    def on_release(self, key):
        if key == keyboard.Key.left:
            self.is_left = False
        elif key == keyboard.Key.right:
            self.is_right = False
        elif key == keyboard.Key.up:
            self.is_forward = False
        elif key == keyboard.Key.down:
            self.is_backward = False
        if key == keyboard.Key.esc: # Exit
            return False
        
        self._send_message()

    def start(self):
        with keyboard.Listener(
        on_press=self.on_press,
        on_release=self.on_release) as listener:
            listener.join()

if __name__ == "__main__":
    bt = Bluetooth("98:D3:91:FD:AB:A4", name="HC-05", passkey="1234", port=1)
    bt.connect()

    c = Controller(bt, verbose=False)
    c.start()

    bt.close()