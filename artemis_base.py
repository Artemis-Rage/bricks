"""ArtemisBase: A DriveBase that tracks its position on the field."""

from pybricks.hubs import PrimeHub
from pybricks.parameters import Stop
from pybricks.robotics import DriveBase

import geometry

hub = PrimeHub()

hub.imu.reset_heading(0)


class ArtemisBase(DriveBase):
    """ArtemisBase a version of DriveBase that tracks its position on the field.
    
    Because ArtemisBase tracks its position, it can drive to specific (x, y)
    coordinates on the field.
    """

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
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
        heading = self.angle()
        turn = (heading - heading) % 360
        if turn > 180:
            turn = turn - 360
        self.turn(turn, then, wait)

    def drive_to(
        self,
        x: float,
        y: float,
        then: Stop = Stop.HOLD,
        wait: bool = True,
    ):
        """Drives from the current location to (x, y)."""
        heading, distance = geometry.compute_trajectory(self.x, self.y, x, y)
        self.turn_to(heading)
        self.straight(distance, then=then, wait=wait)
        self.reset_position(x, y)