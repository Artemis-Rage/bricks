"""Like a record baby..."""

from pybricks.hubs import PrimeHub
from pybricks.parameters import Direction, Port
from pybricks.pupdevices import Motor
from pybricks.tools import multitask, run_task, wait

BIG_GEAR_TEETH = 60
WEE_GEAR_TEETH = 12


hub = PrimeHub()
turntable_motor = Motor(Port.F, gears=[WEE_GEAR_TEETH, BIG_GEAR_TEETH])
left_scanner_motor = Motor(
    Port.D,
    positive_direction=Direction.COUNTERCLOCKWISE,
    gears=[WEE_GEAR_TEETH, BIG_GEAR_TEETH],
)
right_scanner_motor = Motor(
    Port.B,
    positive_direction=Direction.CLOCKWISE,
    gears=[WEE_GEAR_TEETH, BIG_GEAR_TEETH],
)


def init_scanner(angle=30):
    # multitask(
    #     left_scanner_motor.run_until_stall(angle),
    #     right_scanner_motor.reset_angle(angle),
    # )
    left_scanner_motor.reset_angle(angle)
    right_scanner_motor.reset_angle(angle)


async def position_scanner(angle, speed):
    tasks = [
        left_scanner_motor.run_target(speed, angle),
        right_scanner_motor.run_target(speed, angle),
    ]
    await multitask(*tasks)


async def scan_cycle(angles: list[float], orbit=30):
    for a in angles:
        await position_scanner(a, 200)
        print(f"Scanning at angle {a}")
        await wait(orbit * 1000)


async def rotate_turntable(n, orbit=30):
    await turntable_motor.run_angle(360 / orbit, 360 * n)


ORBIT = 10  # seconds
ANGLES = [40, 50, 60, 70, 80, 90]


async def main():
    print(f"{left_scanner_motor.angle()=}, {right_scanner_motor.angle()=}")
    await multitask(scan_cycle(ANGLES, ORBIT), rotate_turntable(len(ANGLES), ORBIT))
    # await multitask(rotate_turntable(len(ANGLES), ORBIT))
    # await rotate_turntable(len(ANGLES), ORBIT)
    print(f"{left_scanner_motor.angle()=}, {right_scanner_motor.angle()=}")


init_scanner(ANGLES[0])
wait(1000)
hub.speaker.beep()
run_task(main())
hub.speaker.beep()
