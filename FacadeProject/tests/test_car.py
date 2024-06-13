import pytest
from car.car import Car

@pytest.fixture
def car():
    return Car()

def test_car_chassis_operation(car):
    car.car.chassis.operation()
    # Add assertions or checks if needed

def test_car_engine_cylinders_operation(car):
    car.car.engine.cylinders.operation()
    # Add assertions or checks if needed

def test_car_engine_pistons_operation(car):
    car.car.engine.pistons.operation()
    # Add assertions or checks if needed
