import RPi.GPIO as GPIO
import time

class ServoMotorInterface():

    def set_servo_x_angle(self, angle):
        if angle > self.settings["ServoMotorXMax"]:
            angle = self.settings["ServoMotorXMax"]

        if angle < self.settings["ServoMotorXMin"]:
            angle = self.settings["ServoMotorXMin"]
        self.xpwm.ChangeDutyCycle(angle)

    def set_servo_y_angle(self, angle):
        if angle > self.settings["ServoMotorYMax"]:
            angle = self.settings["ServoMotorYMax"]
        
        if angle < self.settings["ServoMotorYMin"]:
            angle = self.settings["ServoMotorYMin"]
        self.ypwm.ChangeDutyCycle(angle)

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

