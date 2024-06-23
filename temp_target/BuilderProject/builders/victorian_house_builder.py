from builders.abstract_builder.house_builder import HouseBuilder

class VictorianHouseBuilder(HouseBuilder):
    def build_roof(self):
        self.house.roof = "Victorian Roof"

    def build_interior(self):
        self.house.interior = "Victorian Interior"
