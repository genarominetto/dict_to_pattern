from staff.staff_modules.kitchen import Kitchen
from staff.staff_modules.service import Service

class Staff:
    def __init__(self):
        self.kitchen = Kitchen()
        self.service = Service()
