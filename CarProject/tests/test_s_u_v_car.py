import pytest
from car_builder.builders.s_u_v_car_builder import SUVCarBuilder
from car_builder.director import Director

def test_s_u_v_car():
    builder = SUVCarBuilder()
    director = Director(builder)
    car = director.construct_car()
