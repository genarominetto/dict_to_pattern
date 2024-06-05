import pytest
from car.car import Car

@pytest.fixture
def car():
    return Car()

def test_engine_cylinders_operation(car):
    car.engine.cylinders.operation()
    # Add assertions or checks if needed

def test_engine_pistons_operation(car):
    car.engine.pistons.operation()
    # Add assertions or checks if needed

def test_chassis_operation(car):
    car.chassis.operation()
    # Add assertions or checks if needed

