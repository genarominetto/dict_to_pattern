from dir_a.dir_b.pytest import 
from dir_a.dir_b.vacation_house_builder.builders.rock_mountain_vacation_house_builder import RockMountainVacationHouseBuilder
from dir_a.dir_b.vacation_house_builder.director import Director

def test_rock_mountain_vacation_house():
    builder = RockMountainVacationHouseBuilder()
    director = Director(builder)
    vacation_house = director.construct_vacation_house()

    assert "RockMountain" in str(vacation_house)
    assert "FoundationBase" in str(vacation_house)
    assert "InteriorDesign" in str(vacation_house)
