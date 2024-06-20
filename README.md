# Dict to Pattern

This project provides a scaffolding tool to create complete python programs with tests from simple dictionaries. They are based on design patterns from the book **"Design Patterns: Elements of Reusable Object-Oriented Software."** The end in mind is to create a scaffolder for each design pattern in the book.

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



```

##### How to Use
1. Open the notebook **main.ipynb** on **Google Colab** in the browser.

   [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/GenaroHacker/dict_to_pattern/blob/main/main.ipynb)
2. Run all cells in the notebook.
3. The new program is downloaded automatically if all tests pass.
4. To modify the structure of the program, edit the dictionary `project_structure` in the notebook and re-run the cells.

## Example
**Input:** Dictionary representing the hierarchical structure of the project.

**Output:** Generated file structure adhering to the Facade design pattern.

###### Input
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
#**Note:** In this example, the `main.py` file is considered the facade, not the car or the driver modules. Example methods are implemented by the leaf modules.
