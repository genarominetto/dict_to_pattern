# Facade Scaffolder

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/genarominetto/dict_to_pattern/blob/main/main.ipynb)

### Facade Pattern

- **Definition:** Provide a unified interface to a set of interfaces in a subsystem.
- **Aspects that Vary:** Interface to a subsystem.
- **Participants:** Facade, Subsystem classes.

## Overview
The **Facade Scaffolder** constructs programs that align with the Facade design pattern. Define the project structure using a dictionary to create classes, modules, and tests. The keys in the dictionary represent classes, allowing you to create any tree-like structure.

## How to Use

- Define `project_name`, `project_structure`, and `root_module`.
- Customize `project_structure` to create the desired class hierarchy:
    - Keys represent classes, allowing tree-like structures.


## Example Input:

```python
project_structure = {
    "Car": {
        "Engine": {
            "Cylinders": {},
            "Pistons": {}
        },
        "Chassis": {}
    },
    "Driver": {}
}
```

## Example Output:

### Generated Project Structure:

```
.
├── car
│   ├── car_modules
│   │   ├── engine_modules
│   │   │   ├── cylinders.py
│   │   │   └── pistons.py
│   │   ├── chassis.py
│   │   └── engine.py
│   └── car.py
├── driver
│   └── driver.py
├── tests
│   ├── test_car.py
│   └── test_driver.py
├── main.py
└── pytest.ini
```

### Generated `main.py` file:

```python
from car.car import Car
from driver.driver import Driver

if __name__ == "__main__":
    my_car = Car()
    my_car.engine.cylinders.operation()
    my_car.engine.pistons.operation()
    my_car.chassis.operation()

    my_driver = Driver()
    my_driver.operation()

```

### `main.py` execution output:

```
Cylinders operation executed.
Pistons operation executed.
Chassis operation executed.
Driver operation executed.
```
