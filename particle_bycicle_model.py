

from math import *
import random
# --------
# 
# the "world" has 4 landmarks.
# the robot's initial coordinates are somewhere in the square
# represented by the landmarks.
#
# NOTE: Landmark coordinates are given in (y, x) form and NOT
# in the traditional (x, y) format!

landmarks  = [[0.0, 100.0], [0.0, 0.0], [100.0, 0.0], [100.0, 100.0]] # position of 4 landmarks
world_size = 100.0 # world is NOT cyclic. Robot is allowed to travel "out of bounds"
max_steering_angle = pi/4 # You don't need to use this value, but it is good to keep in mind the limitations of a real car.

# ------------------------------------------------
# 
# this is the robot class
#

class robot:

    # --------

    # init: 
    #	creates robot and initializes location/orientation 
    #

    def __init__(self, length = 10.0):
        self.x = random.random() * world_size # initial x position
        self.y = random.random() * world_size # initial y position
        self.orientation = random.random() * 2.0 * pi # initial orientation
        self.length = length # length of robot
        self.bearing_noise  = 0.0 # initialize bearing noise to zero
        self.steering_noise = 0.0 # initialize steering noise to zero
        self.distance_noise = 0.0 # initialize distance noise to zero
    
    def __repr__(self):
        return '[x=%.6s y=%.6s orient=%.6s]' % (str(self.x), str(self.y), str(self.orientation))
    # --------
    # set: 
    #	sets a robot coordinate
    #

    def set(self, new_x, new_y, new_orientation):

        if new_orientation < 0 or new_orientation >= 2 * pi:
            raise ValueError, 'Orientation must be in [0..2pi]'
        self.x = float(new_x)
        self.y = float(new_y)
        self.orientation = float(new_orientation)


    # --------
    # set_noise: 
    #	sets the noise parameters
    #

    def set_noise(self, new_b_noise, new_s_noise, new_d_noise):
        # makes it possible to change the noise parameters
        # this is often useful in particle filters
        self.bearing_noise  = float(new_b_noise)
        self.steering_noise = float(new_s_noise)
        self.distance_noise = float(new_d_noise)
    

    # --------
    # move:
    #   move along a section of a circular path according to motion
    #
    
    def move(self, motion, tolerance=0.001): # Do not change the name of this function

		#Initialize bycicle model variables
		steering = motion[0]
		distance = motion[1]
		
		#Check coherent fucntion call
		if abs(steering) > max_steering_angle:
			raise ValueError, 'Exceed moving angle'

		if distance < 0.0:
			raise ValueError, 'Robot cant move backwards'

		#Initialize the resulting robot
		res = robot()
		res.length = self.length
		res.bearing_noise = self.bearing_noise
		res.steering_noise = self.steering.noise
		res.distance_noise = self.distance_noise
		
		#Initialize new parameters' noise
		steering2 = random.gauss(steering, steering_noise)
		distance2 = random.gauss(distance, distance_noise)
		
		#Apply motion
		turn = tan(steering2) * distance2/res.length
		
		if abs(turn) < tolerance:
			res.x = self.x + (distance2 * cos(self.orientation))
			res.y = self.y + (distance2 * sin(self.orientation))
			res.orientation =  (self.orientation + turn) % (2*pi)
			
		else:
			#approximate bicycle model for orientation
			R = distance2 / turn
			cx = self.x - sin(self.orientation) * R
			cy = self.y + cos(self.orientation) * R
			res.orientation = (self.orientation + turn) % (2*pi)
			res.x = cx + sin(res.orientation) * R
			res.y = cy - cos(res.orientation) * R
        
        return res


