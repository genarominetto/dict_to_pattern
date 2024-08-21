class Car:
    def __init__(self, car_type):
        self.car_type = car_type
        self.engine = None
        self.wheels = None
        self.body = None

    def set_engine(self, engine):
        self.engine = engine

    def set_wheels(self, wheels):
        self.wheels = wheels

    def set_body(self, body):
        self.body = body

    def __str__(self):
        return (f"Car of type {self.car_type} with "
            f"engine {self.engine}" + f"wheels {self.wheels}" + f"body {self.body}" + ".")
