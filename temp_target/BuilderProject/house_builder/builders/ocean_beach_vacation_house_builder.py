from house_builder.builders.abstract.vacation_house_builder import VacationHouseBuilder
from house_builder.product.vacation_house_parts.foundation_base import FoundationBase
from house_builder.product.vacation_house_parts.interior_design import InteriorDesign

class OceanBeachVacationHouseBuilder(VacationHouseBuilder):
    def __init__(self):
        super().__init__("OceanBeach")
        self.foundation = FoundationBase()
        self.interior = InteriorDesign()

    def build_the_structure(self):
        self.vacation_house.set_structure("OceanBeach_Structure")
        print("Doing build_the_structure for OceanBeach")

    def finalize_details(self):
        self.vacation_house.set_foundation(self.foundation)
        self.vacation_house.set_interior(self.interior)
        print("Doing finalize_details for OceanBeach")
