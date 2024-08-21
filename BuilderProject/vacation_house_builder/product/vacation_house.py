class VacationHouse:
    def __init__(self, vacation_house_type):
        self.vacation_house_type = vacation_house_type
        self.foundation_base = None
        self.interior_design = None

    def set_foundation_base(self, foundation_base):
        self.foundation_base = foundation_base

    def set_interior_design(self, interior_design):
        self.interior_design = interior_design

    def __str__(self):
        return (f"VacationHouse of type {self.vacation_house_type} with "
            f"foundation_base {self.foundation_base}" + f"interior_design {self.interior_design}" + ".")
