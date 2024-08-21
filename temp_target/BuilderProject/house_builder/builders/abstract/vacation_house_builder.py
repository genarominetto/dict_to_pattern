from abc import ABC, abstractmethod
from house_builder.product.vacation_house import VacationHouse

class VacationHouseBuilder(ABC):
    def __init__(self, vacation_house_type):
        self.vacation_house = VacationHouse(vacation_house_type)

    def prepare_the_foundation(self):
        print("Doing prepare_the_foundation")

    def inspect_foundation(self):
        print("Doing inspect_foundation")

    @abstractmethod
    def build_the_structure(self):
        pass

    @abstractmethod
    def finalize_details(self):
        pass

    def get_vacation_house(self):
        return self.vacation_house
