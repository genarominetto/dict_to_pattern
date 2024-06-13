from car.car_modules.chassis import Chassis
from car.car_modules.engine import Engine

class Car:
    def __init__(self):
        self.chassis = Chassis()
        self.engine = Engine()
