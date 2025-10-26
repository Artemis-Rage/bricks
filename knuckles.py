"""Setup code for Knuckles the robot."""

from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Axis, Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

import artemis_base

MOTOR_PROFILE = 5

def setup():
    hub = PrimeHub(
        top_side=-Axis.X,
        front_side=Axis.Z,
    )
    left_drive = Motor(
        Port.E,
        positive_direction=Direction.COUNTERCLOCKWISE,
        profile=MOTOR_PROFILE,
    )
    right_drive = Motor(
        Port.F,
        positive_direction=Direction.CLOCKWISE,
        profile=MOTOR_PROFILE,
    )
    left_tool = Motor(
        Port.C,
        positive_direction=Direction.CLOCKWISE,
        profile=MOTOR_PROFILE,
    )
    right_tool = Motor(
        Port.D,
        positive_direction=Direction.CLOCKWISE,
        profile=MOTOR_PROFILE,
    )
    left_sensor = ColorSensor(Port.A)
    right_sensor = ColorSensor(Port.B)

    base = artemis_base.ArtemisBase(
        left_motor=left_drive,
        right_motor=right_drive,
        wheel_diameter=62.8,
        axle_track=86.7,
    )
    base.settings(
        straight_speed=1000,
        straight_acceleration=1000,
        turn_rate=360,
        turn_acceleration=360,
    )
    base.use_gyro(True)

    return (
        hub,
        base,
        left_drive,
        right_drive,
        left_tool,
        right_tool,
        left_sensor,
        right_sensor,
    )
