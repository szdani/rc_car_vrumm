import bluetooth
import subprocess
import time
import curses
import os

name = "HC-05"   # Device name
addr = "98:D3:91:FD:AB:A4"   # Device Address
port = 1         # RFCOMM port
passkey = "1234" # passkey of the device you want to connect

# kill any "bluetooth-agent" process that is already running
subprocess.call("kill -9 `pidof bt-agent`",shell=True)

# Start a new "bluetooth-agent" process where XXXX is the passkey
#status = subprocess.call("bt-agent " + passkey + " &",shell=True)

# Now, connect in the same way as always with PyBlueZ
#try:
#    s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
#    s.connect((addr,port))
#except bluetooth.btcommon.BluetoothError as err:
#    # Error handler
#    pass

def send_bt_msg(msg, server):
    server.send(msg)
    #r = server.recv(16)
    #time.sleep(0.1)
    return None

def main(win):
    status = subprocess.call("bt-agent " + passkey + " &",shell=True)
    try:
        s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        s.connect((addr,port))
    except bluetooth.btcommon.BluetoothError as err:
        # Error
        print('BT Connection error')
    
    win.nodelay(True)
    key=""
    win.clear()
    win.addstr("Detected key:")
    while True:
        try:
            key = win.getch()
            win.clear()
            win.addstr("Detected key:")
            win.addstr(str(key))
            if key == curses.KEY_LEFT:
                r = send_bt_msg("LEFT", s)
                #win.addstr('\nAnswer {}'.format(r))
            elif key == curses.KEY_RIGHT:
                r = send_bt_msg("RIGHT", s)
                #win.addstr('\nAnswer {}'.format(r))
            else:
                r = send_bt_msg("STOP", s)
                #win.addstr('\nAnswer {}'.format(r))
        except Exception as e:
            #r = send_bt_msg("STOP", s)
            #win.addstr('\nAnswer {}'.format(r))
            pass
        time.sleep(0.25)
    s.close()

curses.wrapper(main)
