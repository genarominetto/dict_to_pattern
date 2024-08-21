from vacation_house_builder.builders.ocean_beach_vacation_house_builder import OceanBeachVacationHouseBuilder
from vacation_house_builder.builders.rock_mountain_vacation_house_builder import RockMountainVacationHouseBuilder
from vacation_house_builder.director import Director

def main():
    ocean_beach_builder = OceanBeachVacationHouseBuilder()
    director = Director(ocean_beach_builder)
    ocean_beach_house = director.construct_vacation_house()
    print(ocean_beach_house)

    rock_mountain_builder = RockMountainVacationHouseBuilder()
    director = Director(rock_mountain_builder)
    rock_mountain_house = director.construct_vacation_house()
    print(rock_mountain_house)

if __name__ == "__main__":
    main()
