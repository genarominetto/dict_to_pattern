from car_builder.builders.sedan_car_builder import SedanCarBuilder
from car_builder.builders.s_u_v_car_builder import SUVCarBuilder
from car_builder.director import Director

def main():
    sedan_builder = SedanCarBuilder()
    director = Director(sedan_builder)
    sedan_car = director.construct_car()
    print(sedan_car)

    s_u_v_builder = SUVCarBuilder()
    director = Director(s_u_v_builder)
    s_u_v_car = director.construct_car()
    print(s_u_v_car)

if __name__ == "__main__":
    main()
