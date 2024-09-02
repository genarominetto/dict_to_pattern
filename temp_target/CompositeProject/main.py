from graphic_drawing.components.leafs.circle import Circle
from graphic_drawing.components.leafs.square import Square
from graphic_drawing.components.composite.group import Group

if __name__ == "__main__":
    # Create individual graphics with name, size, and active status
    circle1 = Circle("Circle1", 5, True)
    square1 = Square("Square1", 4, False)
    circle2 = Circle("Circle2", 7, False)

    # Create groups
    group1 = Group("Group1")
    group2 = Group("Group2")

    # Add graphics to groups
    group1.add(circle1)
    group1.add(square1)

    group2.add(circle2)
    group2.add(group1)

    # Get all nested leaves
    print(f"All nested leaves in group2: {[leaf.name for leaf in group2.get_all_nested_leaves()]}")

    # Get complete structure
    print(f"Structure of group2: {group2.get_structure_as_dict()}")

    # Calculate total size
    print(f"Total size in group2: {group2.calculate_total_size()}")

    # Calculate average size
    average_size = group2.calculate_average_size()
    print(f"Average size in group2: {average_size:.2f}")

    # Check active status
    print(f"Is any graphic in group2 active? {'Yes' if group2.is_active() else 'No'}")

    # Print tree-like structure
    print(f"Tree structure of group2:\n{group2}")
