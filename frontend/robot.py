from time import sleep
import math

from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, MoveTank, SpeedPercent, follow_for_forever, MediumMotor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import ColorSensor, GyroSensor, UltrasonicSensor


class Robot:
    def __init__(self):
        self.tank = MoveTank(OUTPUT_B, OUTPUT_C)
        self.gyro = GyroSensor()
        self.ultrasonic = UltrasonicSensor()
        self.claw = MediumMotor(OUTPUT_A)
        
    def move(self, speed):
        self.tank.follow_gyro_angle(
        kp=11.3, ki=0.05, kd=3.2,
        speed=SpeedPercent(speed),
        target_angle=0,
        follow_for=follow_for_forever
        )
        
    def stop(self):
        self.tank.stop()
        
    def wait(self, seconds):
        sleep(seconds)
        
    def turn(self, degrees):
        target_angle = self.gyro.angle + degrees
        self.tank.on(10, -10)
        while math.abs(self.gyro.angle - target_angle) >= 1:
            pass
        self.stop()
    
    def get_distance(self):
        return self.ultrasonic.distance_inches
    
    def open_claw(self):
        self.claw.on_for_degrees(50)
    
    def close_claw(self):
        self.claw.on_for_degrees(50)
    