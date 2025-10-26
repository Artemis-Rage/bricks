"""ArtemisBase: A DriveBase that tracks its position on the field."""

from pybricks.parameters import Stop
from pybricks.pupdevices import Motor
from pybricks.robotics import DriveBase

import geometry


class Gear:
    FWD = 1
    REV = -1


class ArtemisBase(DriveBase):
    """ArtemisBase a version of DriveBase that tracks its position on the field.
    
    Because ArtemisBase tracks its position, it can drive to specific (x, y)
    coordinates on the field.
    """

    def __init__(
        self,
        left_motor: Motor,
        right_motor: Motor,
        wheel_diameter: float,
        axle_track: float,
        *args,
        **kwargs,
    ):
        super().__init__(
            left_motor,
            right_motor,
            wheel_diameter,
            axle_track,
            *args,
            **kwargs,
        )
        self.reset_position()

    def reset_position(
        self,
        x: float = 0,
        y: float = 0,
    ):
        self.x = x
        self.y = y

    def turn_to(
        self,
        heading: float,
        then: Stop = Stop.HOLD,
        wait: bool = True,
    ):
        """Turns the robot to face in the direction `heading`."""
        current_heading = self.angle()
        turn = (heading - current_heading) % 360
        if turn > 180:
            turn = turn - 360
        self.turn(turn, then, wait)

    def drive_to(
        self,
        x: float,
        y: float,
        then: Stop = Stop.HOLD,
        wait: bool = True,
        gear: Gear = Gear.FWD,
    ):
        """Drives from the current location to (x, y)."""
        heading, distance = geometry.compute_trajectory(self.x, self.y, x, y)
        if gear == Gear.REV:
            heading += 180
            distance = -distance
        self.turn_to(heading)
        self.straight(distance, then=then, wait=wait)
        self.reset_position(x, y)
