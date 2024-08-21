import pytest
from car_builder.builders.sedan_car_builder import SedanCarBuilder
from car_builder.director import Director

def test_sedan_car():
    builder = SedanCarBuilder()
    director = Director(builder)
    car = director.construct_car()
