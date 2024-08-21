from car_builder.builders.abstract.car_builder import CarBuilder
from car_builder.product.car import Car
from car_builder.product.car_parts.engine import Engine
from car_builder.product.car_parts.wheels import Wheels
from car_builder.product.car_parts.body import Body

class SUVCarBuilder(CarBuilder):
    def __init__(self):
        super().__init__("SUV")
        self.car = Car("SUV")
        self.engine = Engine()
        self.car.set_engine(self.engine)
        self.wheels = Wheels()
        self.car.set_wheels(self.wheels)
        self.body = Body()
        self.car.set_body(self.body)

    def attach_wheels(self):
        print("Doing attach_wheels for SUV")

    def paint_body(self):
        print("Doing paint_body for SUV")
