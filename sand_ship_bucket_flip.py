from pybricks.hubs import PrimeHub
from pybricks.tools import wait

from alpha import AttachmentAlpha
from artemis_base_v2 import ArtemisBase, Gear

WEST_START = dict(
    x=350,
    y=140,
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


class SandPull:
    start = WEST_START
    forward_point = dict(x=350, y=400)
    shipwreck = dict(x=726, y=95)
    shipwreck_heading = 90
    right_arm_speed = 200
    right_arm_down = 90
    right_arm_up = 0
    pull_back = dict(x=680, y=95)
    end = dict(x=680, y=95)

    def run(
        self,
        robot: ArtemisBase,
        attachment: AttachmentAlpha,
    ) -> None:
        # Robot should be in starting position.
        assert robot.x == WEST_START["x"]
        assert robot.y == WEST_START["y"]
        
        # Loop the robot back to the Shipwreck
        robot.drive_to(**self.forward_point)
        
        # Drive to Shipwreck
        robot.drive_to(**self.shipwreck, gear=Gear.REV)
        
        # Turn
        robot.turn_to(self.shipwreck_heading)
        
        # Arm Down
        attachment.right_arm_move(
            speed=self.right_arm_speed,
            position=self.right_arm_down,
        )
        
        # Drive Backward to pull the sand
        robot.drive_to(**self.pull_back, gear=Gear.REV)
        
        # Lift arm
        attachment.right_arm_move(
            speed=self.right_arm_speed,
            position=self.right_arm_up,
        )


class ShipPush:
    start = dict(x=680, y=95)
    push_position = dict(x=770, y=243)
    push_end = dict(x=967, y=243)
    back_position = dict(x=785, y=243)
    turn_heading = 120
    slow_arm_speed = 100
    fast_arm_speed = 200
    arm_down_position = 70
    arm_up_position = 5
    backward_distance = 100
    reset_position = dict(x=698, y=290)

    def run(
        self,
        robot: ArtemisBase,
        attachment: AttachmentAlpha,
    ) -> None:
        # Driving to where you push up the ship
        robot.drive_to(**self.push_position)
        
        # Pushing up the ship
        robot.drive_to(**self.push_end)
        
        # Moving back
        robot.drive_to(**self.back_position, gear=Gear.REV)
        
        # Turning to an angle
        robot.turn_to(self.turn_heading)
        
        # Dropping arm (flag drop)
        attachment.left_arm_move(
            speed=self.slow_arm_speed,
            position=self.arm_down_position,
        )
        
        # Moving back again
        robot.straight(-self.backward_distance)
        robot.reset_position(**self.reset_position)
        
        # Arm up
        attachment.left_arm_move(
            speed=self.fast_arm_speed,
            position=self.arm_up_position,
        )


class BucketFlip:
    start = dict(x=698, y=290)
    bucket_approach = dict(x=1225, y=600)
    right_arm_speed = 200
    right_arm_positions = [75, 5]
    end = dict(x=1225, y=600)

    def run(
        self,
        robot: ArtemisBase,
        attachment: AttachmentAlpha,
    ) -> None:
        # Moving to bucket
        robot.drive_to(**self.bucket_approach)
        
        # Flip bucket
        attachment.right_arm_move(
            speed=self.right_arm_speed,
            position=self.right_arm_positions[0],
        )
        attachment.right_arm_move(
            speed=self.right_arm_speed,
            position=self.right_arm_positions[1],
        )


class HoopPull:
    start = dict(x=1225, y=600)
    bucket_position = dict(x=1196, y=530)
    skewer_heading_1 = 90
    right_arm_speed = 200
    skewer_arm_position = 95
    skewer_heading_2 = 180
    skewer_heading_3 = -75
    final_skewer = dict(x=1120, y=540)
    arm_up_position = 5
    home_position = dict(x=1980, y=120)

    def run(
        self,
        robot: ArtemisBase,
        attachment: AttachmentAlpha,
    ) -> None:
        # Position robot to skewer hoop
        robot.drive_to(**self.bucket_position)
        robot.turn_to(self.skewer_heading_1)
        
        attachment.right_arm_move(
            speed=self.right_arm_speed,
            position=self.skewer_arm_position,
        )
        
        robot.turn_to(self.skewer_heading_2)
        robot.turn_to(self.skewer_heading_3)
        
        robot.drive_to(**self.final_skewer)
        
        # Lift arm
        attachment.right_arm_move(
            speed=self.right_arm_speed,
            position=self.arm_up_position,
        )
        
        # Return home
        robot.drive_to(**self.home_position, gear=Gear.REV)

class GoHome:
    positions = [
        dict(x=1980, y=120),
    ]
    def run(
        self,
        robot: ArtemisBase,
        attachment: AttachmentAlpha,
    ) -> None:
        for position in self.positions:
            robot.drive_to(**position, gear=Gear.REV)


if __name__ == "__main__":
    hub, robot, attachment = init()
    SandPull().run(robot, attachment)
    ShipPush().run(robot, attachment)
    BucketFlip().run(robot, attachment)
    HoopPull().run(robot, attachment)
    GoHome().run(robot, attachment)
