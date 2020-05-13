import bluetooth, subprocess

name = "HC-05"   # Device name
addr = "98:D3:91:FD:AB:A4"   # Device Address
port = 1         # RFCOMM port
passkey = "1234" # passkey of the device you want to connect

# kill any "bluetooth-agent" process that is already running
subprocess.call("kill -9 `pidof bt-agent`",shell=True)

# Start a new "bluetooth-agent" process where XXXX is the passkey
status = subprocess.call("bt-agent " + passkey + " &",shell=True)

# Now, connect in the same way as always with PyBlueZ
try:
    s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    s.connect((addr,port))
except bluetooth.btcommon.BluetoothError as err:
    # Error handler
    pass

import time
while True:
    time.sleep(5)
    s.send("LEFT")
    time.sleep(0.25)
    r = s.recv(1024)
    print(r)
    #time.sleep(5)
    s.send("RIGHT")
    time.sleep(0.25)
    r = s.recv(1024)
    print(r)

    s.send('LED OFF')
    time.sleep(0.25)
    r = s.recv(1024)
    print(r)

s.close()
