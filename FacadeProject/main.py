from car.car import Car

if __name__ == "__main__":
    my_car = Car()
    my_car.engine.cylinders.operation()
    my_car.engine.pistons.operation()
    my_car.chassis.operation()
