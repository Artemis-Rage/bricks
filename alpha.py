from pybricks.pupdevices import Motor


_LEFT_ARM_DOWN_ANGLE = 99
_RIGHT_ARM_DOWN_ANGLE = -81
_STALL_DUTY_LIMIT = 30

class AttachmentAlpha:
    def __init__(
        self,
        left_motor: Motor,
        right_motor: Motor,
    ):
        self.left_motor = left_motor
        self.right_motor = right_motor

    def left_arm_init(self):
        self.left_motor.run_until_stalled(
            -200,
            duty_limit=_STALL_DUTY_LIMIT,
        )
        self.left_motor.reset_angle(0)

    def right_arm_init(self):
        self.right_motor.run_until_stalled(
            200,
            duty_limit=_STALL_DUTY_LIMIT,
        )
        self.right_motor.reset_angle(0)

    def init(self):
        self.left_arm_init()
        self.right_arm_init()

    def left_arm_move(self, speed, position):
        angle = position / 100 * _LEFT_ARM_DOWN_ANGLE
        self.left_motor.run_target(
            speed=speed,
            target_angle=angle,
        )

    def right_arm_move(self, speed, position):
        angle = position / 100 * _RIGHT_ARM_DOWN_ANGLE
        self.right_motor.run_target(
            speed=speed,
            target_angle=angle,
        )