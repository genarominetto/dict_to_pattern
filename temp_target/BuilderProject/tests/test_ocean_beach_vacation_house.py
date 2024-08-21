import pytest
from house_builder.builders.ocean_beach_vacation_house_builder import OceanBeachVacationHouseBuilder
from house_builder.director import Director

def test_ocean_beach_vacation_house():
    builder = OceanBeachVacationHouseBuilder()
    director = Director(builder)
    vacation_house = director.construct_vacation_house()
    
    assert "OceanBeach" in str(vacation_house)
    assert "FoundationBase" in str(vacation_house)
    assert "InteriorDesign" in str(vacation_house)
