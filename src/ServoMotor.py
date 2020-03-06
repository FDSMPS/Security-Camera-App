'''
    Creation Date: Feb 3, 2020
    Author: Tymoore Jamal
    Content: This file contains the Servo Motor class which handles the motion detectors.
'''

import RPi.GPIO as GPIO
import time

class ServoMotorInterface():
    '''
        The ServoMotor class. Controlls both servo motors.
    '''
    def set_servo_x_angle(self, angle):
        '''
            Sets the servo's X angle
            @param angle: the angle to set
        '''
        # self.start_servo_x()

        if angle > self.settings["ServoMotorXMax"]:
            angle = self.settings["ServoMotorXMax"]

        if angle < self.settings["ServoMotorXMin"]:
            angle = self.settings["ServoMotorXMin"]
        self.xpwm.ChangeDutyCycle(angle)

        # self.stop_servo_x()


    def set_servo_y_angle(self, angle):
        '''
            Sets the servo's Y angle
            @param angle: the angle to set
        '''

        # self.start_servo_y()

        if angle > self.settings["ServoMotorYMax"]:
            angle = self.settings["ServoMotorYMax"]
        
        if angle < self.settings["ServoMotorYMin"]:
            angle = self.settings["ServoMotorYMin"]
        self.ypwm.ChangeDutyCycle(angle)

        # self.stop_servo_y()


    def start_servo_x(self):
        self.xpwm.start(0)

    def start_servo_y(self):
        self.ypwm.start(0)

    def stop_servo_x(self):
        self.xpwm.stop()

    def stop_servo_y(self):
        self.ypwm.stop()


    def __init__(self, settings):
        '''
            Creates an instance of this class and initialzes its class variables.
            @param settings: the settings found in the config file.
        '''
        self.settings = settings

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        GPIO.setup(self.settings["ServoMotorXPin"], GPIO.OUT)
        GPIO.setup(self.settings["ServoMotorYPin"], GPIO.OUT)

        self.xpwm = GPIO.PWM(self.settings["ServoMotorXPin"], 50)
        self.ypwm = GPIO.PWM(self.settings["ServoMotorYPin"], 50)

        self.start_servo_x()
        self.start_servo_y()


