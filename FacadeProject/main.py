from menu.menu import Menu
from staff.staff import Staff

if __name__ == "__main__":
    my_menu = Menu()
    my_menu.food.appetizers.operation()
    my_menu.food.maincourse.operation()
    my_menu.drinks.alcoholic.operation()
    my_menu.drinks.nonalcoholic.operation()

    my_staff = Staff()
    my_staff.kitchen.chefs.operation()
    my_staff.kitchen.helpers.operation()
    my_staff.service.waiters.operation()
    my_staff.service.managers.operation()

