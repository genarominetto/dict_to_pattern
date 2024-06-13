from menu.menu_modules.drinks_modules.alcoholic import Alcoholic
from menu.menu_modules.drinks_modules.nonalcoholic import NonAlcoholic

class Drinks:
    def __init__(self):
        self.alcoholic = Alcoholic()
        self.nonalcoholic = NonAlcoholic()
