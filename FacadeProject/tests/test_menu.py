import pytest
from menu.menu import Menu

@pytest.fixture
def menu():
    return Menu()

def test_menu_drinks_alcoholic_operation(menu):
    menu.menu.drinks.alcoholic.operation()
    # Add assertions or checks if needed

def test_menu_drinks_nonalcoholic_operation(menu):
    menu.menu.drinks.nonalcoholic.operation()
    # Add assertions or checks if needed

def test_menu_food_appetizers_operation(menu):
    menu.menu.food.appetizers.operation()
    # Add assertions or checks if needed

def test_menu_food_maincourse_operation(menu):
    menu.menu.food.maincourse.operation()
    # Add assertions or checks if needed
