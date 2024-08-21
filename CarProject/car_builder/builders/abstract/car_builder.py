from abc import ABC
from abc import abstractmethod
from car_builder.product.car import Car

class CarBuilder(ABC):
    def __init__(self, car_type):
        self.car = Car(car_type)

    def assemble_chassis(self):
        print("Doing assemble_chassis")

    def install_engine(self):
        print("Doing install_engine")

    @abstractmethod
    def attach_wheels(self):
        pass

    @abstractmethod
    def paint_body(self):
        pass

    def get_car(self):
        return self.car
