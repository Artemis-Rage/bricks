"""Draft of a logging library."""

from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Axis, Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import multitask, StopWatch, run_task, wait

class MotorEntry:
    __slots__ = (
        'name',
        'time',
        'angle',
        'speed',
        'load',
    )
    
    def __init__(
        self,
        name: str,
        time: float,
        angle: float,
        speed: float,
        load: float,
    ):
        self.name = name
        self.time = time
        self.angle = angle
        self.speed = speed
        self.load = load
    
    def dump(self):
        yield f'{self.name},{self.time},angle,{self.angle}'
        yield f'{self.name},{self.time},speed,{self.speed}'
        yield f'{self.name},{self.time},load,{self.load}'
        
        
class HubEntry:
    __slots__ = (
        'time',
        'acceleration_x',
        'acceleration_y',
        'acceleration_z',
        'angular_velocity_x',
        'angular_velocity_y',
        'angular_velocity_z',
        'heading',
    )
    
    def __init__(
        self,
        name: str,
        time: float,
        acceleration_x: float,
        acceleration_y: float,
        acceleration_z: float,
        angular_velocity_x: float,
        angular_velocity_y: float,
        angular_velocity_z: float,
        heading: float,
    ):
        self.name = name
        self.time = time
        self.acceleration_x = acceleration_x
        self.acceleration_y = acceleration_y
        self.acceleration_z = acceleration_z
        self.angular_velocity_x = angular_velocity_x
        self.angular_velocity_y = angular_velocity_y
        self.angular_velocity_z = angular_velocity_z
        self.heading = heading
    
    def dump(self):
        yield f'{self.name},{self.time},acceleration_x,{self.acceleration_x}'
        yield f'{self.name},{self.time},acceleration_y,{self.acceleration_y}'
        yield f'{self.name},{self.time},acceleration_z,{self.acceleration_z}'
        yield f'{self.name},{self.time},angular_velocity_x,{self.angular_velocity_x}'
        yield f'{self.name},{self.time},angular_velocity_y,{self.angular_velocity_y}'
        yield f'{self.name},{self.time},angular_velocity_z,{self.angular_velocity_z}'
        yield f'{self.name},{self.time},heading,{self.heading}'


class Logger:
    
    start_token = '<START LOGS>'
    end_token = '<END LOGS>'

    def __init__(
        self,
        hubs: dict[str, PrimeHub],
        motors: dict[str, Motor],
        interval_ms: int = 100,
    ):
        self.hubs = hubs
        self.motors = motors
        self.interval_ms = interval_ms
        self.running = False
        self.entries = []
        self.watch = StopWatch()
        
    async def _log_motor(
        self,
        name: str,
        motor: Motor,
        time: float
    ) -> MotorEntry:
        motor.model.state()
        return MotorEntry(
            name=name,
            time=time,
            angle=motor.angle(),
            speed=motor.speed(window=300),
            load=motor.load(),
        )
        
    async def _log_hub(
        self,
        name: str,
        hub: PrimeHub,
        time: float,
    ) -> HubEntry:
        imu = hub.imu
        ax, ay, az = imu.acceleration()
        avx, avy, avz = imu.angular_velocity()
        return HubEntry(
            name=name,
            time=time,
            acceleration_x=ax,
            acceleration_y=ay,
            acceleration_z=az,
            angular_velocity_x=avx,
            angular_velocity_y=avy,
            angular_velocity_z=avz,
            heading=imu.heading(),
        )
        

    async def _logging_loop(self):
        while self.running:
            time = self.watch.time()
            log_actions = [
                self._log_motor(name, motor, time)
                for name, motor in self.motors.items()
            ] + [
                self._log_hub(name, hub, time)
                for name, hub in self.hubs.items()
            ]
            _, *entries = await multitask(
                wait(self.interval_ms),
                *log_actions,
            )
            self.entries.extend(entries)
            
    def run_with_logging(self, coro):
        self.running = True
        run_task(multitask(self._logging_loop(), coro, race=True))
        self.running = False
        
    def dump(self):
        for entry in self.entries:
            yield from entry.dump()

    def print(self):
        print(self.start_token)
        print('device,time,parameter,value')
        for entry in self.entries:
            for line in  entry.dump():
                print(line)
        print(self.end_token)


            


        
        
        
        
