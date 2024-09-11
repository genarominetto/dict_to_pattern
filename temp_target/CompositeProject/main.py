from component.components.composite.group import Group
from component.components.leafs.circle import Circle
from component.components.leafs.square import Square

if __name__ == "__main__":
    circle1 = Circle(name="Circle1", size=3, is_active=True)
    circle2 = Circle(name="Circle2", size=3, is_active=True)
    square1 = Square(name="Square1", size=3, is_active=True)
    square2 = Square(name="Square2", size=3, is_active=True)
    
    group1 = Group(name="Group1")
    group2 = Group(name="Group2")

    group1.add(circle1)
    group1.add(square1)
    group2.add(circle2)
    group2.add(square2)

    group1.remove(square1)

    group1.add(group2)
    
    def get_graphic_name(graphic):
        return graphic.name
    
    circle_names = group1.execute_operation_recursively(
        operation_func=get_graphic_name,
        condition_func=isinstance,
        condition_args=(Circle,)
    )
    depth = group1.calculate_depth()
    
    print(group1)
    print(group1.is_composite())
    print(group1.any_active())
    print(group1.id)
    print(len(group1.get_children()))
    print(circle_names)
    print(depth)

