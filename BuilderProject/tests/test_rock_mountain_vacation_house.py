import pytest
from vacation_house_builder.builders.rock_mountain_vacation_house_builder import RockMountainVacationHouseBuilder
from vacation_house_builder.director import Director

def test_rock_mountain_vacation_house():
    builder = RockMountainVacationHouseBuilder()
    director = Director(builder)
    vacation_house = director.construct_vacation_house()
