from abc import ABC, abstractmethod
from product.house import House

class HouseBuilder(ABC):
    def __init__(self):
        self.house = House()

    def build_foundation(self):
        self.house.foundation = "Generic Foundation"

    def build_structure(self):
        self.house.structure = "Generic Structure"

    @abstractmethod
    def build_roof(self):
        pass

    @abstractmethod
    def build_interior(self):
        pass

    def get_house(self):
        return self.house
