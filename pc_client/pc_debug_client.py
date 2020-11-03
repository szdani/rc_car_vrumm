import bt as bt
from tkinter import *

import time

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib import gridspec


import numpy as np
import math

import matplotlib.pyplot as plt

import logging
logging.basicConfig(format='%(asctime)s | %(name)s | %(levelname)s | %(message)s', 
                    datefmt='%m/%d/%Y %I:%M:%S %p', 
                    level=logging.INFO)

from car_position import CarPosition


class PositionCanvas(FigureCanvasTkAgg):
    '''Matplotlib based TK canvas to display the 
    position and the rotation of the car.
    '''
    def __init__(self, figure, master):
        FigureCanvasTkAgg.__init__(self, figure, master=master)
        
        self.positions_x = [0]
        self.positions_y = [0]
        self.distances_x = []
        self.distances_y = []

        self.figure = figure
        spec = gridspec.GridSpec(ncols=2, nrows=1,
                         width_ratios=[3, 1])
        self.map_subplot = figure.add_subplot(spec[0])
        self.orientation_plot = figure.add_subplot(spec[1])
        self.map_subplot.tick_params(axis='x', labelsize=6)
        self.map_subplot.tick_params(axis='y', labelsize=6, labelrotation=90 )
        
        self.orientation_plot.get_xaxis().set_visible(False)
        self.orientation_plot.get_yaxis().set_visible(False)
        self.orientation_plot.set_ylim(-1,1)
        self.orientation_plot.set_xlim(-1,1)
        self.orientation_plot.set_autoscale_on(False)
        
        plt.subplots_adjust(left=0, bottom=0, right=0.1, top=0.1, wspace=0, hspace=0)
        self.map_subplot.plot(self.positions_x, self.positions_y)
        self.draw()

    def add_new_position(self, x, y, orientation, plot=True):
        self.distances_x.append(self.positions_x[-1] - x)
        self.distances_y.append(self.positions_y[-1] - y)

        self.positions_x.append(x)
        self.positions_y.append(y)

        if plot:
            # TODO: change matplotlib to 2D rendering
            self.map_subplot.cla()

            self.map_subplot.quiver(self.positions_x[:-1], self.positions_y[:-1], 
                                self.distances_x, self.distances_y,
                                alpha=0.8, color='green',
                                angles='xy', scale_units='xy', scale=1)
            self.map_subplot.scatter( self.positions_x[-1], self.positions_y[-1], c='red', marker='x')

            o_x = math.sin(orientation)
            o_y = math.cos(orientation)
            self.orientation_plot.cla()
            self.orientation_plot.scatter([0, 1, 1, -1, -1],[0, 1, -1, 1, -1], c='red')
            self.orientation_plot.plot([0, o_x],[0, o_y], c='green')
            self.orientation_plot.arrow(0, 0, o_x, o_y)
            self.draw()


class App(Frame):
    def __init__(self, master=None, bt_connection=None):
        Frame.__init__(self, master)
        self.master = master
        self.bt_connection = bt_connection
        self.connection_flag = False
        self.broker = bt.BluetoothBroker(bt_connection)
        self.position = CarPosition()

        ######
        # GUI
        ######
        self.connect_button = Button(master, text = 'Connect BT', command = self.connect)
        self.connect_button.place(x=20, y=10)

        self.disconnect_button = Button(master, text = 'Disconn BT', command = self.disconnect)
        self.disconnect_button.place(x=125, y=10)
        self.disconnect_button["state"] = "disabled"

        self.text = Text(master, height=10, width=70)
        self.text.place(x=0, y=80)
        self.vsb = Scrollbar(master, orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")

        self.frame = Frame(self.master, borderwidth = 2, relief = "groove")
        self.frame.place(bordermode = "outside", relwidth = 0.96, relheight = 0.5, relx = 0., rely = 0.48, x = 5, y = 5, anchor = "nw")
        self.frame.canvas = Frame(self.frame, borderwidth = 0)
        self.frame.canvas.place(relwidth = 1, relheight = 1, relx = 0, anchor = "nw")
        self.fig = Figure(figsize = (9.6, 5), facecolor = "white")
        self.fig.set_tight_layout({"pad": .0})
        
        self.canvas = PositionCanvas(self.fig, master = self.frame.canvas)
        self.canvas.get_tk_widget().pack()


    def connect(self):
        '''Connect button callback. Connects to BT module.
        '''
        try:
            self.bt_connection.connect()
            self.connection_flag = True
            self.connect_button["state"] = "disabled"
            self.disconnect_button["state"] = "normal"
        except Exception as e:
            self.label.configure(text='Connection error: {}'.format(e))
            return
        logging.info('Connected BT')
        self.broker.subscribe('DIS', self.process_distance_frame)
        self.broker.subscribe(bt.BluetoothBroker.ALL_TOPICS, self.snoop)
        self.broker.start()

    def disconnect(self):
        '''Disconnect button callback. Exits BT connection.
        '''
        self.bt_connection.close()
        self.connection_flag = False
        self.connect_button["state"] = "normal"
        self.disconnect_button["state"] = "disabled"

    def snoop(self, topicObj=bt.BluetoothBroker.AUTO_TOPIC, **mesgData):
        '''Subscriber callback for debugging. Prints out every message on every topic.
        '''
        self.text.insert("end", ('"%s": %s' % (topicObj.getName(), mesgData)) + "\n")
        self.text.see("end")
        logging.debug(('BT MSG: "%s": %s' % (topicObj.getName(), mesgData)))

    def process_distance_frame(self, message):
        '''Subscriber callback for distance sensor messages. Updates the position of
        the car based on the incoming data. Canvas will be updated also.
        Format:"%d;%d;%d;%d", 
            leftFallingCounter, leftRisingCounter, rightFallingCounter, rightRisingCounter
        '''
        frame = message.split(';')

        frame = [int(x) for x in frame if x is not '']
        logging.debug('Distance {}'.format(frame))

        left_falling = frame[0]
        left_raising = frame[1]

        right_falling = frame[2]
        right_rising = frame[3]

        x, y, o = self.position.update_based_on_counters(left_raising, left_falling, right_rising, right_falling )

        self.canvas.add_new_position(x, y, o, plot=True)


if __name__ == "__main__":
    bt_connection = bt.Bluetooth("98:D3:91:FD:AB:A4", name="HC-05", passkey="1234", port=1)

    root = Tk()
    app=App(root, bt_connection=bt_connection)
    root.wm_title("Car Debug GUI")
    root.geometry("600x600")
    logging.info('App started!')
    root.mainloop() 