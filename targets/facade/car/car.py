from car.subsystems.engine import Engine
from car.subsystems.wheels import Wheels

class Car(Engine, Wheels):
    def __init__(self):
        Engine.__init__(self)
        Wheels.__init__(self)
