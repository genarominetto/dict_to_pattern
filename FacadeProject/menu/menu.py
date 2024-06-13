from menu.menu_modules.drinks import Drinks
from menu.menu_modules.food import Food

class Menu:
    def __init__(self):
        self.drinks = Drinks()
        self.food = Food()
