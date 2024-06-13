import pytest
from car.car import Car

@pytest.fixture
def car():
    return Car()

def test_engine_operation(car):
    car.engine.operation()
    # Add assertions or checks if needed

def test_chassis_operation(car):
    car.chassis.operation()
    # Add assertions or checks if needed
