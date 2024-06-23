from builders.abstract_builder.house_builder import HouseBuilder

class ModernHouseBuilder(HouseBuilder):
    def build_roof(self):
        self.house.roof = "Modern Roof"

    def build_interior(self):
        self.house.interior = "Modern Interior"
