# Composite Scaffolder

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/genarominetto/dict_to_pattern/blob/main/main.ipynb)


### Composite Pattern

- **Definition:** Lets clients treat individual objects and compositions of objects uniformly.
- **Aspects that Vary:** Structure and composition of an object.
- **Participants:** Component, Leaf, Composite.

## Overview

The **Composite Scaffolder** constructs programs that align with the Composite design pattern. Modify the `project_structure` dict values to customize the program as needed.

## How to Use

- Define `project_name`, `project_structure`, and `root_module`.
- Customize `project_structure` to set desired classes and methods:
    - `component`, `composite`, and `leaves` represent Python classes.
    - `leaf_properties` represents properties within component classes.

## Example Input:

```python
project_structure = {
    "component": "Graphic",
    "composite": "Group",
    "leaves": ["Circle", "Square"],
    "leaf_properties": {
        "size": 3,
        "is_active": True
    }
}
```

## Example Output:

### Generated Project Structure:

```
.
├── graphic
│   ├── abstract
│   │   ├── graphic_modules
│   │   │   ├── data_loader.py
│   │   │   └── graphic_validator.py
│   │   └── graphic.py
│   ├── components
│   │   ├── composite
│   │   │   └── group.py
│   │   ├── leaves
│   │   │   ├── abstract
│   │   │   │   └── leaf.py
│   │   │   ├── circle.py
│   │   │   └── square.py
│   ├── tests
│   │   ├── test_circle.py
│   │   └── test_square.py
├── main.py
└── pytest.ini
```

### Generated `main.py` file:

```python
from graphic.components.composite.group import Group

from graphic.components.leaves.circle import Circle

from graphic.components.leaves.square import Square


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

    group1.remove(circle1)

    group1.add(group2)

    def get_graphic_name(graphic):
        return graphic.name

    circle_names = group1.execute_operation_recursively(
        operation_func=get_graphic_name,
        condition_func=isinstance,
        condition_args=(Circle,),
    )
    depth = group1.calculate_depth()

    print(group1)
    print(f"Is group1 composite? {group1.is_composite()})")

    print(f"Does group1 have any active elements? {group1.any_active()})")

    print(f"Group1 ID: {group1.id})")
    print(f"Number of children in group1: {len(group1.get_children())})")
    print(f"Circle names in group1: {circle_names})")
    print(f"Depth of group1 hierarchy: {depth})")

```

### `main.py` execution output:

```
Group1/
├── Square1(size: 3, is_active: True)
└── Group2/
    ├── Circle2(size: 3, is_active: True)
    └── Square2(size: 3, is_active: True)

Is group1 composite? True)
Does group1 have any active elements? True)
Group1 ID: 5)
Number of children in group1: 2)
Circle names in group1: ['Circle2'])
Depth of group1 hierarchy: 3)
```
