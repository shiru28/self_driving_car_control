#!/usr/bin/env python3

import cutils
import numpy as np
import math

class Controller2D(object):
    def __init__(self, waypoints):
        self.vars                = cutils.CUtils()
        self._current_x          = 0
        self._current_y          = 0
        self._current_yaw        = 0
        self._current_speed      = 0
        self._desired_speed      = 0
        self._current_frame      = 0
        self._current_timestamp  = 0
        self._start_control_loop = False
        self._set_throttle       = 0
        self._set_brake          = 0
        self._set_steer          = 0
        self._waypoints          = waypoints
        self._conv_rad_to_steer  = 180.0 / 70.0 / np.pi
        self._pi                 = np.pi
        self._2pi                = 2.0 * np.pi
        self._L                  = 2.0

    def update_values(self, x, y, yaw, speed, timestamp, frame):
        self._current_x         = x
        self._current_y         = y
        self._current_yaw       = yaw
        self._current_speed     = speed
        self._current_timestamp = timestamp
        self._current_frame     = frame
        if self._current_frame:
            self._start_control_loop = True

    def update_desired_speed(self):
        min_idx       = 0
        min_dist      = float("inf")
        desired_speed = 0
        for i in range(len(self._waypoints)):
            dist = np.linalg.norm(np.array([
                    self._waypoints[i][0] - self._current_x,
                    self._waypoints[i][1] - self._current_y]))
            if dist < min_dist:
                min_dist = dist
                min_idx = i
        if min_idx < len(self._waypoints)-1:
            desired_speed = self._waypoints[min_idx][2]
        else:
            desired_speed = self._waypoints[-1][2]
        self._desired_speed = desired_speed

    def update_waypoints(self, new_waypoints):
        self._waypoints = new_waypoints

    def get_commands(self):
        return self._set_throttle, self._set_steer, self._set_brake

    def set_throttle(self, input_throttle):
        # Clamp the throttle command to valid bounds
        throttle           = np.fmax(np.fmin(input_throttle, 1.0), 0.0)
        self._set_throttle = throttle

    def set_steer(self, input_steer_in_rad):
        # Covnert radians to [-1, 1]
        input_steer = self._conv_rad_to_steer * input_steer_in_rad

        # Clamp the steering command to valid bounds
        steer           = np.fmax(np.fmin(input_steer, 1.0), -1.0)
        self._set_steer = steer

    def set_brake(self, input_brake):
        # Clamp the steering command to valid bounds
        brake           = np.fmax(np.fmin(input_brake, 1.0), 0.0)
        self._set_brake = brake

    def update_controls(self):
        x               = self._current_x
        y               = self._current_y
        yaw             = self._current_yaw
        v               = self._current_speed
        self.update_desired_speed()
        v_desired       = self._desired_speed
        t               = self._current_timestamp
        waypoints       = self._waypoints
        throttle_output = 0
        steer_output    = 0
        brake_output    = 0

        self.vars.create_var('t_prev', 0.0)
        
        # Longitudinal Control Gains
        kp = 0.7
        ki = 0.02
        kd = 0.05
        
        # Variables for longitudinal control
        self.vars.create_var('v_error_prev', 0.0)
        self.vars.create_var('v_error_integral_prev', 0.0)
        v_error = v_desired - v
        
        # Variables for lateral control
        fx = x + self._L * np.cos(yaw)/2.0
        fy = y + self._L * np.sin(yaw)/2.0
                                          
        # Lateral Control Gains       
        kp_heading = 10
               
        # Skip the first frame to store previous values properly
        if self._start_control_loop:
            """
                Controller iteration code block.

                Controller Feedback Variables:
                    x               : Current X position (meters)
                    y               : Current Y position (meters)
                    yaw             : Current yaw pose (radians)
                    v               : Current forward speed (meters per second)
                    t               : Current time (seconds)
                    v_desired       : Current desired speed (meters per second)
                                      (Computed as the speed to track at the
                                      closest waypoint to the vehicle.)
                    waypoints       : Current waypoints to track
                                      (Includes speed to track at each x,y
                                      location.)
                                      Format: [[x0, y0, v0],
                                               [x1, y1, v1],
                                               ...
                                               [xn, yn, vn]]
                                      Example:
                                          waypoints[2][1]: 
                                          Returns the 3rd waypoint's y position

                                          waypoints[5]:
                                          Returns [x5, y5, v5] (6th waypoint)
                
                Controller Output Variables:
                    throttle_output : Throttle output (0 to 1)
                    steer_output    : Steer output (-1.22 rad to 1.22 rad)
                    brake_output    : Brake output (0 to 1)
            """

            ################################################
            ##   Implementation of Longitudinal Control   ##
            ################################################
            v_error_integral = self.vars.v_error_integral_prev + v_error
            v_error_rate_of_change = (v_error - self.vars.v_error_prev) / (t - self.vars.t_prev)
            
            # Change these outputs with the longitudinal controller. Note that
            # brake_output is optional and is not required to pass the
            # assignment, as the car will naturally slow down over time.
            throttle_output = kp * v_error + ki * v_error_integral + kd * v_error_rate_of_change
            if throttle_output < 0.0:
                brake_output = throttle_output
                throttle_output = 0.0
            
            ###########################################
            ##   Implementation of Lateral Control   ##
            ###########################################
            dx = []
            dy = []
            for i in range(len(waypoints)):
                dx.append(fx - waypoints[i][0])
                dy.append(fy - waypoints[i][1])
            d = np.hypot(dx, dy)
            target_idx = np.argmin(d)
            if target_idx <= len(waypoints) - 2:
                d_y_desired = waypoints[target_idx + 1][1] - waypoints[target_idx][1]
                d_x_desired = waypoints[target_idx + 1][0] - waypoints[target_idx][0]
            
            if abs(d_x_desired) <= math.pow(10,-4):
                d_x_desired = -abs(d_x_desired)
         
            crosstrack_error = np.dot([dx[target_idx], dy[target_idx]],[-np.cos(yaw + np.pi/2), -np.sin(yaw + np.pi/2)])
            
            crosstrack_heading = np.arctan2(kp_heading * crosstrack_error, v)
            
            crosstrack_heading_error = np.arctan2(d_y_desired, d_x_desired) - yaw
            
            # Change the steer output with the lateral controller.             
            steer_output = crosstrack_heading_error + crosstrack_heading
            
            # Set Control Outputs
            self.set_throttle(throttle_output)  # in percent (0 to 1)
            self.set_steer(steer_output)        # in rad (-1.22 to 1.22)
            self.set_brake(brake_output)        # in percent (0 to 1)

        self.vars.t_prev = t
        self.vars.v_error_prev = v_error
        self.vars.v_error_integral_prev = v_error_integral