from car.car_modules.engine_modules.cylinders import Cylinders
from car.car_modules.engine_modules.pistons import Pistons

class Engine:
    def __init__(self):
        self.cylinders = Cylinders()
        self.pistons = Pistons()
