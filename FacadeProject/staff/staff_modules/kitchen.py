from staff.staff_modules.kitchen_modules.chefs import Chefs
from staff.staff_modules.kitchen_modules.helpers import Helpers

class Kitchen:
    def __init__(self):
        self.chefs = Chefs()
        self.helpers = Helpers()
