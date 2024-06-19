# Dict to Pattern
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/GenaroHacker/dict_to_pattern/blob/main/main.ipynb)

## Overview
This project provides a scaffolding tool for creating code structures based on design patterns from the book **"Design Patterns: Elements of Reusable Object-Oriented Software."** The end in mind is to create a scaffolder for each design pattern in the book.

## Table of Contents
1. [Progress](#progress)
2. [Patterns](#patterns)
   - [Facade](#facade)
     - [Project Structure](#project-structure)
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

## Patterns

### Creational Patterns

### Structural Patterns

#### Facade

##### Project Structure
```
dict_to_pattern
├── skaffolders
│   └── facade
│       ├── modules
│       │   ├── helpers
│       │   │   └── helper.py
│       │   ├── branch_file_creator.py
│       │   ├── leaf_file_creator.py
│       │   ├── main_file_creator.py
│       │   ├── simple_file_creator.py
│       │   └── test_file_creator.py
│       └── project_creator.py
├── jupyter.py
├── main.ipynb
└── README.md
```

##### How to Use
1. Open the notebook **main.ipynb** on **Google Colab** in the browser.

   [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/GenaroHacker/dict_to_pattern/blob/main/main.ipynb)
2. Run all cells in the notebook.
3. The new program automatically downloads if all tests pass.
4. To modify the structure of the program, edit the dictionary in the notebook and re-run the cells.

##### Example

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

### Behavioral Patterns

