from pybricks.hubs import PrimeHub
from pybricks.tools import wait

from alpha import AttachmentAlpha
from artemis_base_v2 import ArtemisBase, Gear

WEST_START = dict(
    x=359,
    y=137,
)


def init() -> tuple[PrimeHub, ArtemisBase, AttachmentAlpha]:
    hub, robot = ArtemisBase.default()
    attachment = AttachmentAlpha(
        left_motor=robot.left_attachment,
        right_motor=robot.right_attachment,
    )
    robot.reset_position(**WEST_START)
    attachment.init()
    return hub, robot, attachment


class SurfaceBrushing:
    start = WEST_START
    forward_point = dict(x=WEST_START["x"], y=800)
    end = dict(x=WEST_START["x"], y=600)


    def run(
        self,
        robot: ArtemisBase,
        attachment: AttachmentAlpha,
    ) -> None:
        # Robot should be in starting position.
        assert robot.x == WEST_START["x"]
        assert robot.y == WEST_START["y"]
        robot.drive_to(**self.forward_point)
        robot.drive_to(**self.end, gear=Gear.REV)


class MapReveal:
    start = dict(x=498, y=796)
    soil_heading = -43
    left_arm_speed = 200
    right_arm_speed = 200
    left_arm_positions = [100, 5]
    right_arm_positions = [55, 95, 5]
    slow_speed = 150
    slow_acceleration = 200
    step_sizes = [95, 30]
    end = dict(x=507, y=787)

    def run(
        self,
        robot: ArtemisBase,
        attachment: AttachmentAlpha,
    ) -> None:
        robot.drive_to(**self.start)
        robot.turn_to(self.soil_heading)
        attachment.left_arm_move(
            speed=self.left_arm_speed,
            position=self.left_arm_positions[0],
        )
        attachment.right_arm_move(
            speed=self.right_arm_speed,
            position=self.right_arm_positions[0],
        )
        robot.straight(
            self.step_sizes[0],
            speed=self.slow_speed,
            acceleration=self.slow_acceleration,
        )
        attachment.right_arm_move(
            speed=self.right_arm_speed,
            position=self.right_arm_positions[1],
        )
        robot.straight(
            self.step_sizes[1],
            speed=self.slow_speed,
            acceleration=self.slow_acceleration,
        )
        attachment.right_arm_move(
            speed=self.right_arm_speed,
            position=self.right_arm_positions[2],
        )
        robot.straight(
            -sum(self.step_sizes),
        )
        attachment.left_arm_move(
            speed=self.left_arm_speed,
            position=self.left_arm_positions[1],
        )
        robot.drive_to(**self.end, gear=Gear.REV)


class Mineshaft:
    start = dict(x=550, y=915)
    lift_location = dict(x=620, y=915)
    arm_speed = 200
    down_position = 75
    up_position = 0
    wait_time = 800

    def run(
        self,
        robot: ArtemisBase,
        attachment: AttachmentAlpha,
    ) -> None:
        robot.drive_to(**self.start)
        attachment.left_arm_move(
            speed=self.arm_speed,
            position=self.down_position,
        )
        robot.drive_to(**self.lift_location)
        attachment.left_arm_move(
            speed=self.arm_speed,
            position=self.up_position,
        )
        wait(self.wait_time)
        attachment.left_arm_move(
            speed=self.arm_speed,
            position=self.down_position,
        )


class Statue:
    start = dict(x=759, y=824)
    lift_heading = 152
    forward_distance = 70
    wait_time = 200
    arm_speed = 200
    left_arm_positions = [100, 40, 20]
    right_arm_positions = [20, 60]
    twist_heading = 135
    backward_distance = 200

    def run(
        self,
        robot: ArtemisBase,
        attachment: AttachmentAlpha,
    ) -> None:
        robot.drive_to(**self.start)
        robot.turn_to(self.lift_heading)
        attachment.left_arm_move(
            speed=self.arm_speed,
            position=self.left_arm_positions[0],
        )
        robot.straight(self.forward_distance)
        attachment.left_arm_move(
            speed=self.arm_speed,
            position=self.left_arm_positions[1],
        )
        wait(self.wait_time)
        robot.turn_to(self.twist_heading)
        wait(self.wait_time)
        attachment.left_arm_move(
            speed=self.arm_speed,
            position=self.left_arm_positions[2],
        )
        wait(self.wait_time)
        attachment.right_arm_move(
            speed=self.arm_speed,
            position=self.right_arm_positions[0],
        )
        wait(self.wait_time)
        robot.straight(-self.backward_distance)

class GoHome:
    positions = [
        dict(x=380, y=220),
    ]

    def run(
        self,
        robot: ArtemisBase,
        attachment: AttachmentAlpha,
    ) -> None:
        for position in self.positions:
            robot.drive_to(**position)


if __name__ == "__main__":
    hub, robot, attachment = init()
    SurfaceBrushing().run(robot, attachment)
    MapReveal().run(robot, attachment)
    Mineshaft().run(robot, attachment)
    Statue().run(robot, attachment)
    GoHome().run(robot, attachment)
