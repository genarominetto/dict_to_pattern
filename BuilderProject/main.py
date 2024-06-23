from builders.modern_house_builder import ModernHouseBuilder
from builders.victorian_house_builder import VictorianHouseBuilder
from director.director import ConstructionDirector

if __name__ == "__main__":
    modern_builder = ModernHouseBuilder()
    director = ConstructionDirector(modern_builder)
    modern_house = director.construct_house()
    print("Modern House built:", modern_house.show())

    victorian_builder = VictorianHouseBuilder()
    director = ConstructionDirector(victorian_builder)
    victorian_house = director.construct_house()
    print("Victorian House built:", victorian_house.show())
