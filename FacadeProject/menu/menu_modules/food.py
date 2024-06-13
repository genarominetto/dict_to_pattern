from menu.menu_modules.food_modules.appetizers import Appetizers
from menu.menu_modules.food_modules.maincourse import MainCourse

class Food:
    def __init__(self):
        self.appetizers = Appetizers()
        self.maincourse = MainCourse()
