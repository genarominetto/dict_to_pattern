import pytest
from dir_a.dir_b.vacation_house_builder.builders.ocean_beach_vacation_house_builder import OceanBeachVacationHouseBuilder
from dir_a.dir_b.vacation_house_builder.director import Director

def test_ocean_beach_vacation_house():
    builder = OceanBeachVacationHouseBuilder()
    director = Director(builder)
    vacation_house = director.construct_vacation_house()
