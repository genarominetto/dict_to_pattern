from car.car_modules.engine import Engine
from car.car_modules.chassis import Chassis

class Car:
    def __init__(self):
        self.engine = Engine()
        self.chassis = Chassis()
