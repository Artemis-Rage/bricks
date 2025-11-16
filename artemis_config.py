"""Configuration classes for Artemis Base."""

class ToleranceConfig:
    def __init__(
        self,
        speed: float,
        position: float,
    ):
        self.speed = speed
        self.position = position

    def __repr__(self):
        return f"{self.__class__.__name__}(speed={self.speed!r}, position={self.position!r})"


class ControlConfig:
    def __init__(
        self,
        kp: float,
        ki: float,
        kd: float,
        heading_tolerance: ToleranceConfig,
        distance_tolerance: ToleranceConfig,
    ):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.heading_tolerance = heading_tolerance
        self.distance_tolerance = distance_tolerance

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"kp={self.kp!r}, ki={self.ki!r}, kd={self.kd!r}, "
            f"heading_tolerance={self.heading_tolerance!r}, "
            f"distance_tolerance={self.distance_tolerance!r}"
            f")"
        )


class MotionConfig:
    def __init__(
        self,
        straight_speed: float,
        straight_acceleration: float,
        turn_rate: float,
        turn_acceleration: float,
    ):
        self.straight_speed = straight_speed
        self.straight_acceleration = straight_acceleration
        self.turn_rate = turn_rate
        self.turn_acceleration = turn_acceleration

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"straight_speed={self.straight_speed!r}, "
            f"straight_acceleration={self.straight_acceleration!r}, "
            f"turn_rate={self.turn_rate!r}, "
            f"turn_acceleration={self.turn_acceleration!r}"
            f")"
        )

class GeometryConfig:
    def __init__(
        self,
        wheel_diameter: float,
        axle_track: float,
    ):
        self.wheel_diameter = wheel_diameter
        self.axle_track = axle_track

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"wheel_diameter={self.wheel_diameter!r}, "
            f"axle_track={self.axle_track!r}"
            f")"
        )

class ToleranceConfig:
    def __init__(
        self,
        speed: float,
        position: float,
    ):
        self.speed = speed
        self.position = position

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"speed={self.speed!r}, position={self.position!r}"
            f")"
        )


class ArtemisConfig:
    def __init__(
        self,
        geometry_config: GeometryConfig,
        motion_config: MotionConfig,
        straight_control_config: ControlConfig,
        turn_control_config: ControlConfig,
    ):
        self.geometry_config = geometry_config
        self.motion_config = motion_config
        self.straight_control_config = straight_control_config
        self.turn_control_config = turn_control_config

    @classmethod
    def default(cls):
        return cls(
            geometry_config=GeometryConfig(
                wheel_diameter=63,
                axle_track=81,
            ),
            motion_config=MotionConfig(
                straight_speed=350,
                straight_acceleration=800,
                turn_rate=150,
                turn_acceleration=500,
            ),
            straight_control_config=ControlConfig(
                kp=18_500,
                ki=410,
                kd=100,
                heading_tolerance=ToleranceConfig(
                    speed=38,
                    position=1,
                ),
                distance_tolerance=ToleranceConfig(
                    speed=27,
                    position=2,
                ),
            ),
            turn_control_config=ControlConfig(
                kp=11_000,
                ki=17_000,
                kd=2_100,
                heading_tolerance=ToleranceConfig(
                    speed=38,
                    position=2,
                ),
                distance_tolerance=ToleranceConfig(
                    speed=27,
                    position=2,
                ),
            ),
        )

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"geometry_config={self.geometry_config!r}, "
            f"motion_config={self.motion_config!r}, "
            f"straight_control_config={self.straight_control_config!r}, "
            f"turn_control_config={self.turn_control_config!r}"
            f")"
        )