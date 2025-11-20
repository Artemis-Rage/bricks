"""ArtemisBase: A DriveBase that tracks its position on the field.

The recommended way to instantiate an ArtemisBase is

```
hub, robot = ArtemisBase.default()
```
"""

from pybricks.parameters import Stop
from pybricks.pupdevices import ColorSensor, Motor
from pybricks.robotics import DriveBase
from pybricks.hubs import PrimeHub
from pybricks.parameters import Axis, Direction, Port
from pybricks.tools import multitask, run_task, wait

import artemis_config
import geometry


class Gear:
    FWD = 'FWD'
    REV = 'REV'


def get_hub():
    return PrimeHub(top_side=Axis.Z, front_side=Axis.Y)


class ArtemisBase(DriveBase):
    """ArtemisBase a version of DriveBase that tracks its position on the field.

    Because ArtemisBase tracks its position, it can drive to specific (x, y)
    coordinates on the field.
    """

    def __init__(
        self,
        left_drive: Motor,
        right_drive: Motor,
        left_attachment: Motor,
        right_attachment: Motor,
        left_color: ColorSensor,
        right_color: ColorSensor,
        config: artemis_config.ArtemisConfig,
    ):

        super().__init__(
            left_drive,
            right_drive,
            config.geometry_config.wheel_diameter,
            config.geometry_config.axle_track,
        )
        self.left_drive = left_drive
        self.right_drive = right_drive
        self.left_attachment = left_attachment
        self.right_attachment = right_attachment
        self.left_color = left_color
        self.right_color = right_color
        self.geometry = config.geometry_config
        self.motion = config.motion_config
        self.straight_control = config.straight_control_config
        self.turn_control = config.turn_control_config
        self.use_gyro(True)
        self.reset_position()

    def _config_global(self):
        self.settings(
            straight_speed=self.motion.straight_speed,
            straight_acceleration=self.motion.straight_acceleration,
            turn_rate=self.motion.turn_rate,
            turn_acceleration=self.motion.turn_acceleration,
        )

    def _configure_straight_control(self):
        self._config_global()
        self.heading_control.pid(
            kp=self.straight_control.kp,
            ki=self.straight_control.ki,
            kd=self.straight_control.kd,
        )
        self.heading_control.target_tolerances(
            speed=self.straight_control.heading_tolerance.speed,
            position=self.straight_control.heading_tolerance.position,
        )
        self.distance_control.target_tolerances(
            speed=self.straight_control.distance_tolerance.speed,
            position=self.straight_control.distance_tolerance.position,
        )

    def _configure_turn_control(self):
        self._config_global()
        self.heading_control.pid(
            kp=self.turn_control.kp,
            ki=self.turn_control.ki,
            kd=self.turn_control.kd,
        )
        self.heading_control.target_tolerances(
            speed=self.turn_control.heading_tolerance.speed,
            position=self.turn_control.heading_tolerance.position,
        )
        self.distance_control.target_tolerances(
            speed=self.turn_control.distance_tolerance.speed,
            position=self.turn_control.distance_tolerance.position,
        )

    def reset_position(
        self,
        x: float = 0,
        y: float = 0,
    ):
        self.x = x
        self.y = y

    async def _straight_with_timeout(
        self,
        distance: float,
        timeout: float,
        then: Stop = Stop.HOLD,
    ):        
        await multitask(
            super().straight(
                distance=distance,
                then=then,
            ),
            wait(timeout),
            race=True,
        )

    def straight(
        self,
        distance: float,
        then: Stop = Stop.HOLD,
        wait: bool = True,
        speed: float | None = None,
        acceleration: float | None = None,
        timeout: float | None = None,
    ):
        """Drives straight for a given distance.
        
        Args:
            distance: The distance to drive in millimeters.
            then: The action to take after driving.
            wait: Whether to wait for the drive to complete.
            speed: Override the global speed setting.
            acceleration: Override the global acceleration setting.
            timeout: If set, the maximum time to allow for the movement
                before stopping it, in milliseconds.
        """
        self._configure_straight_control()
        if speed is not None:
            self.settings(straight_speed=speed)
        if acceleration is not None:
            self.settings(straight_acceleration=acceleration)
        if timeout is not None:
            run_task(
                self._straight_with_timeout(
                    distance=distance,
                    timeout=timeout,
                    then=then,
                )
            )
        else:
            super().straight(
                distance=distance,
                then=then,
                wait=wait,
            )
        new_x, new_y = geometry.compute_new_position(
            self.x,
            self.y,
            self.angle(),
            distance,
        )
        self.reset_position(new_x, new_y)

    async def _turn_with_timeout(
        self,
        angle: float,
        timeout: float,
        then: Stop = Stop.HOLD,
    ):
        await multitask(
            self.turn(
                angle=angle,
                then=then,
            ),
            wait(timeout),
            race=True,
        )

    def turn_to(
        self,
        heading: float,
        then: Stop = Stop.HOLD,
        wait: bool = True,
        speed: float | None = None,
        acceleration: float | None = None,
        timeout: float | None = None,
    ):
        """Turns the robot to face in the direction `heading`.

        Args:
            heading: The heading to turn to in degrees.
            then: The action to take after turning.
            wait: Whether to wait for the turn to complete.
            speed: Override the global turn speed setting.
            acceleration: Override the global turn acceleration setting.
            timeout: If set, the maximum time to allow for the movement
                before stopping it, in milliseconds.
        """
        self._configure_turn_control()
        if speed is not None:
            self.settings(turn_rate=speed)
        if acceleration is not None:
            self.settings(turn_acceleration=acceleration)
        current_heading = self.angle()
        turn = (heading - current_heading) % 360
        if turn > 180:
            turn = turn - 360
        if timeout is not None:
            run_task(
                self._turn_with_timeout(
                    angle=turn,
                    timeout=timeout,
                    then=then,
                )
            )
        else:
            self.turn(turn, then, wait)

    def drive_to(
        self,
        x: float,
        y: float,
        then: Stop = Stop.HOLD,
        wait: bool = True,
        gear: Gear = Gear.FWD,
        timeout: float | None = None,
    ):
        """Drives from the current location to (x, y)."""
        heading, distance = geometry.compute_trajectory(
            self.x, self.y, x, y,
        )
        if gear == Gear.REV:
            heading += 180
            distance = -distance
        self.turn_to(heading, timeout=timeout)
        self.straight(distance, then=then, wait=wait, timeout=timeout)
        # Assume we've arrived at the destination rather than using the
        # computation from `straight`.
        self.reset_position(x, y)

    @classmethod
    def default(cls) -> tuple[PrimeHub, "ArtemisBase"]:
        hub = get_hub()
        left_drive = Motor(Port.A, Direction.COUNTERCLOCKWISE)
        right_drive = Motor(Port.E, Direction.CLOCKWISE)
        left_attachment = Motor(Port.D, Direction.CLOCKWISE)
        right_attachment = Motor(Port.C, Direction.CLOCKWISE)
        left_color = ColorSensor(Port.B)
        right_color = ColorSensor(Port.F)
        robot = cls(
            left_drive=left_drive,
            right_drive=right_drive,
            left_attachment=left_attachment,
            right_attachment=right_attachment,
            left_color=left_color,
            right_color=right_color,
            config=artemis_config.ArtemisConfig.default(),
        )
        robot.use_gyro(True)
        return hub, robot
