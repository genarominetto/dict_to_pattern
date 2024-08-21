from car_builder.builders.abstract.car_builder import CarBuilder

class Director:
    def __init__(self, builder: CarBuilder):
        self.builder = builder

    def construct_car(self):
        self.builder.assemble_chassis()
        self.builder.install_engine()
        self.builder.attach_wheels()
        self.builder.paint_body()
        return self.builder.get_car()
