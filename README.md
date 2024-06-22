# Dict to Pattern

This is a scaffolding tool to create complete python template programs with tests from simple dictionaries. They are based on design patterns from the book **"Design Patterns: Elements of Reusable Object-Oriented Software."** The end in mind is to create a scaffolder for each design pattern in the book.

Currently, it only supports the **Facade** design pattern.

## TO GET STARTED, **PRESS** THE "OPEN IN COLAB" BUTTON AND **RUN** EVERY CELL.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/GenaroHacker/dict_to_pattern/blob/main/main.ipynb)

## Table of Contents
1. [Progress](#progress)
2. [Patterns](#patterns)
   - [Facade](#facade)
     - [How to Use](#how-to-use)
     - [Example](#example)
       - [Input](#input)
       - [Output](#output)

## Progress

### Creational Patterns
- [ ] Abstract Factory
- [ ] Builder
- [ ] Factory Method
- [ ] Prototype
- [ ] Singleton

### Structural Patterns
- [ ] Adapter
- [ ] Bridge
- [ ] Composite
- [x] **Facade**
- [ ] Flyweight
- [ ] Proxy
- [ ] Decorator

### Behavioral Patterns
- [ ] Chain of Responsibility
- [ ] Command
- [ ] Interpreter
- [ ] Iterator
- [ ] Mediator
- [ ] Memento
- [ ] Observer
- [ ] State
- [ ] Strategy
- [ ] Template Method
- [ ] Visitor

# Patterns

# Facade
**Definition:** Provide a unified interface to a set of interfaces in a subsystem.

**Aspects that Vary:** Interface to a subsystem.

**Participants:** Facade, Subsystem classes.




##### How to Use
1. Open the notebook **main.ipynb** on **Google Colab** in the browser.

   [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/GenaroHacker/dict_to_pattern/blob/main/main.ipynb)
2. Run all cells in the notebook.
3. The new program is downloaded automatically if all tests pass.
4. To modify the structure of the program, edit the dictionary `project_structure` in the notebook and re-run the cells.

## Example




###### Input
**Input:** Dictionary representing the hierarchical structure of the project.
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
#**Note:** Any tree structure is supported. Modules with an empty dict value are considered leaf modules.
###### Output
**Output:** Generated file structure adhering to the Facade design pattern.
```
FacadeProject
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


# What to expect?
### Generated Files

Main File (main.py):
The main file initializes core objects and invokes their primary operations.

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

Branch File (car.py):
A branch file defines the structure of complex objects, containing the initialization of various components.

```python
from car.car_modules.chassis import Chassis
from car.car_modules.engine import Engine

class Car:
    def __init__(self):
        self.chassis = Chassis()
        self.engine = Engine()
```
Leaf File (cylinders.py):
A leaf file represents a simple component, performing basic operations.

```python
class Cylinders:
    def __init__(self):
        pass

    def operation(self):
        print("Cylinders operation executed.")

```

Test File (test_car.py):
A test file contains unit tests for verifying the functionality of the code using pytest.

```python
import pytest
from car.car import Car

@pytest.fixture
def car():
    return Car()

def test_car_chassis_operation(car):
    car.chassis.operation()
    # Add assertions or checks if needed

def test_car_engine_cylinders_operation(car):
    car.engine.cylinders.operation()
    # Add assertions or checks if needed

def test_car_engine_pistons_operation(car):
    car.engine.pistons.operation()
    # Add assertions or checks if needed

```




