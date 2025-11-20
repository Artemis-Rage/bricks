"""ArtemisBase: A DriveBase that tracks its position on the field."""

from pybricks.hubs import PrimeHub
from pybricks.parameters import Stop
from pybricks.robotics import DriveBase

import geometry

hub = PrimeHub()

hub.imu.reset_heading(0)


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
        straight_kp, straight_ki, straight_kd = 18500, 410, 100
        straight_heading_speed, straight_heading_position = 38, 5
        straight_distance_speed, straight_distance_position = 27, 5

        turn_kp, turn_ki, turn_kd = 12000, 21000, 3000
        turn_heading_speed, turn_heading_position = 38, 5
        turn_distance_speed, turn_distance_position = 27, 5

        ''' set PID values for turn '''
        self.heading_control.pid(kp=turn_kp, ki=turn_ki, kd=turn_kd) # set straight PID
        self.heading_control.target_tolerances(speed=turn_heading_speed, position=turn_heading_position) # set straight heading tolerance
        self.distance_control.target_tolerances(speed=turn_distance_speed, position=turn_distance_position) # set straight distance tolerance

        current_heading = self.angle()
        turn = (heading - current_heading) % 360
        if turn > 180:
            turn = turn - 360
        self.turn(turn, then, wait)

        '''set PID values for straight'''
        self.heading_control.pid(kp=straight_kp, ki=straight_ki, kd=straight_kd) # set straight PID
        self.heading_control.target_tolerances(speed=straight_heading_speed, position=straight_heading_position) # set straight heading tolerance
        self.distance_control.target_tolerances(speed=straight_distance_speed, position=straight_distance_position) # set straight distance tolerance

    def drive_to(
        self,
        x: float,
        y: float,
        then: Stop = Stop.HOLD,
        wait: bool = True,
        gear: Gear = Gear.FWD,
    ):
        """Drives from the current location to (x, y)."""
        straight_kp, straight_ki, straight_kd = 18500, 410, 100
        straight_heading_speed, straight_heading_position = 38, 5
        straight_distance_speed, straight_distance_position = 27, 5

        '''set PID values for straight'''
        self.heading_control.pid(kp=straight_kp, ki=straight_ki, kd=straight_kd) # set straight PID
        self.heading_control.target_tolerances(speed=straight_heading_speed, position=straight_heading_position) # set straight heading tolerance
        self.distance_control.target_tolerances(speed=straight_distance_speed, position=straight_distance_position) # set straight distance tolerance
        heading, distance = geometry.compute_trajectory(self.x, self.y, x, y)
        if gear == Gear.REV:
            heading += 180
            distance=-distance

        self.turn_to(heading)
        self.straight(distance, then=then, wait=wait)
        self.reset_position(x, y)
