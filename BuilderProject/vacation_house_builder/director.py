from dir_a.dir_b.vacation_house_builder.builders.abstract.vacation_house_builder import VacationHouseBuilder

class Director:
    def __init__(self, builder: VacationHouseBuilder):
        self.builder = builder

    def construct_vacation_house(self):
        self.builder.prepare_the_foundation()
        self.builder.inspect_foundation()
        self.builder.build_the_structure()
        self.builder.finalize_details()
        return self.builder.get_vacation_house()
