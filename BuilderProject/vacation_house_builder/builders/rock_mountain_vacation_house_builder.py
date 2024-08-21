from vacation_house_builder.builders.abstract.vacation_house_builder import VacationHouseBuilder
from vacation_house_builder.product.vacation_house_parts.foundation_base import FoundationBase
from vacation_house_builder.product.vacation_house_parts.interior_design import InteriorDesign

class RockMountainVacationHouseBuilder(VacationHouseBuilder):
    def __init__(self):
        super().__init__("RockMountain")
        self.foundation_base = FoundationBase()
        self.interior_design = InteriorDesign()

    def build_the_structure(self):
        print("Doing build_the_structure for RockMountain")

    def finalize_details(self):
        print("Doing finalize_details for RockMountain")
