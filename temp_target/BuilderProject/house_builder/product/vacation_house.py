class VacationHouse:
    def __init__(self, vacation_house_type):
        self.vacation_house_type = vacation_house_type
        self.foundation = None
        self.structure = None
        self.interior = None

    def set_foundation(self, foundation):
        self.foundation = foundation

    def set_structure(self, structure):
        self.structure = structure

    def set_interior(self, interior):
        self.interior = interior

    def __str__(self):
        return (f"VacationHouse of type {self.vacation_house_type} with "
                f"foundation {self.foundation}, structure {self.structure}, "
                f"and interior {self.interior}.")
