from pybricks.hubs import PrimeHub

from alpha import AttachmentAlpha
from artemis_base import ArtemisBase, Gear
from map import WEST_START


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
    start = dict(x=350, y=450)
    forward_point = dict(x=350, y=800)
    end = dict(x=350, y=600)


    def run(
        self,
        robot: ArtemisBase,
        attachment: AttachmentAlpha,
    ) -> None:
        robot.drive_to(**self.start)
        robot.drive_to(**self.forward_point)
        robot.drive_to(**self.end, gear=Gear.REV)


class MapReveal:
    start = dict(x=350, y=800)
    soil_location = dict(x=497, y=793)
    soil_heading = -42
    left_arm_speed = 200
    right_arm_speed = 200
    left_arm_positions = [100, 5]
    right_arm_positions = [60, 95, 5]
    slow_speed = 150
    slow_acceleration = 200
    step_sizes = [95, 45]
    end = dict(x=503, y=787)

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
        robot.drive_to(**self.end)


class Mineshaft:
    # This used to be 550, 900. Is there a reason it was different
    # from lift_position?
    start = dict(x=550, y=905)
    lift_location = dict(x=620, y=905)
    arm_speed = 200
    down_position = 75
    up_position = 0
    wait_time = 1000
    end = dict(x=620, y=905)

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
        robot.drive_to(**self.end)


class Statue:
    start = dict(x=757, y=788)
    lift_location = dict(x=782, y=742)
    lift_heading = 153
    backup_distance = 100
    wait_times = [100, 200]
    slow_arm_speed = 200
    fast_arm_speed = 1000
    left_arm_positions = [100, 0]
    right_arm_positions = [60, 5]
    end = dict(x=450, y=250)

    def run(
        self,
        robot: ArtemisBase,
        attachment: AttachmentAlpha,
    ) -> None:
        robot.drive_to(**self.start)
        attachment.left_arm_move(
            speed=self.slow_arm_speed,
            position=self.left_arm_positions[0],
        )
        robot.drive_to(**self.lift_location)
        robot.turn_to(self.lift_heading)
        attachment.left_arm_move(
            speed=self.fast_arm_speed,
            position=self.left_arm_positions[1],
        )
        wait(self.wait_times[0])
        attachment.right_arm_move(
            speed=self.slow_arm_speed,
            position=self.right_arm_positions[0],
        )
        wait(self.wait_times[1])
        robot.straight(-self.backup_distance)
        attachment.right_arm_move(
            speed=self.fast_arm_speed,
            position=self.right_arm_positions[1],
        )
        robot.drive_to(**self.end)

if __name__ == "__main__":
    hub, robot, attachment = init()
    SurfaceBrushing().run(robot, attachment)
    MapReveal().run(robot, attachment)
    Mineshaft().run(robot, attachment)
    Statue().run(robot, attachment)
