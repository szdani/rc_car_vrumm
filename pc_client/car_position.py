import numpy as np
import math

import logging
logging.basicConfig(format='%(asctime)s | %(name)s | %(levelname)s | %(message)s', 
                    datefmt='%m/%d/%Y %I:%M:%S %p', 
                    level=logging.INFO)

class CarPosition():
    #AXIS_SIZE = 180 #mm
    #HALF_AXIS_SIZE = 90 #mm
    # 20 holes
    # d(car tires) = 65mm r=32.5mm
    # Circumference = 204.2mm
    # 1 hole -> 18 degrees
    # 1 degree -> 0.5672mm
    # 18 degrees -> 10.2102mm
    # 1 hole -> 10.2102mm
    # TODO refine constants with error calc.

    DEBUG_MAX_COUNTER_DIFF_ONE_SIDE = 5
    DEGREE_PER_HOLES = 18
    DISTANCE_PER_HOLES = 10.2102

    def __init__(self, x=0, y=0, orientation=0):
        self.x = x
        self.y = y
        self.xy_history = []
        self.orientation = orientation

    def _average_counters(self, raising, falling):
        if abs(raising - falling) >= self.DEBUG_MAX_COUNTER_DIFF_ONE_SIDE:
            logging.error("To big difference between falling and raising counters! F: {} R: {}".format(falling, raising))
        return (raising + falling)/2

    def _is_clockwise_rotation(self, left, right):
        '''Assumes that thhe movement is a rotation! 
        True if the rotation is clockwise! (positive)
        '''
        return (left > 0 and right < 0)

    def _is_rotation(self, left, right):
        return (left < 0 and right > 0) or (left > 0 and right < 0)
    
    def _calculate_rotation(self, left, right):
        if self._is_clockwise_rotation(left, right):
            avg = self._average_counters(left, -right)
            degree = self.DEGREE_PER_HOLES * avg
        else:
            avg = self._average_counters(-left, right)
            degree = -self.DEGREE_PER_HOLES * avg
        return degree

    def _calculate_distance(self, left, right):
        distance = self._average_counters(left, right)
        distance = self.DISTANCE_PER_HOLES * distance
        x = distance*math.sin(self.orientation)
        y = distance*math.cos(self.orientation)
        return x, y

    def update_based_on_counters(self, left_raising, left_falling, right_rising, right_falling ):
        self.xy_history.append([self.x, self.y])

        avg_left = self._average_counters(left_raising, left_falling)
        avg_right = self._average_counters(right_rising, right_falling)
        if self._is_rotation(avg_left, avg_right):
            degree = self._calculate_rotation(avg_left, avg_right)
            self.orientation += degree
            logging.info("Rotation with {} degree = {}degree".format(degree, self.orientation))
        else: # forward or backward
            x, y = self._calculate_distance(avg_left, avg_right)
            self.x += x
            self.y += y
            logging.info("Movement with {}:{} mm (x:y)".format(x,y))
            
        return self.x, self.y, self.orientation