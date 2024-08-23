# Builder Scaffolder

## Overview
The **Builder Scaffolder** constructs programs that align with the Builder design pattern. Define the project structure using the dict `project_structure` to create classes, methods, and tests. Modify the dict values to customize the program as needed.

## How to Use

- **Set Up Project**:
    - Define `project_name`, `project_structure`, and `root_module`.
    - Customize `project_structure` to set desired classes and methods:
        - `product`, `types`, and `parts` represent Python classes.
        - `parent_steps` and `child_steps` represent methods within builder classes.

## Example Input:

    ```python
    project_name = "BuilderProject"
    project_structure = {
        "product": "Airplane",
        "types": ["CommercialJet", "PrivateJet"],
        "parts": ["Fuselage", "Wings", "Wheels"],
        "parent_steps": ["build_fuselage", "attach_wings"],
        "child_steps": ["install_interior", "test_flight"]
    }
    root_module = ""
    ```

## Example Output:

### Project Structure:

```
.
├── airplane_builder
│   ├── builders
│   │   ├── abstract
│   │   │   └── airplane_builder.py
│   │   ├── commercial_jet_airplane_builder.py
│   │   └── private_jet_airplane_builder.py
│   ├── product
│   │   ├── airplane_parts
│   │   │   ├── fuselage.py
│   │   │   ├── wheels.py
│   │   │   └── wings.py
│   │   └── airplane.py
│   └── director.py
├── tests
│   ├── test_commercial_jet_airplane.py
│   └── test_private_jet_airplane.py
├── main.py
└── pytest.ini
```

### `main.py`:

```python
from airplane_builder.builders.commercial_jet_airplane_builder import CommercialJetAirplaneBuilder
from airplane_builder.builders.private_jet_airplane_builder import PrivateJetAirplaneBuilder
from airplane_builder.director import Director

def main():
    commercial_jet_builder = CommercialJetAirplaneBuilder()
    director = Director(commercial_jet_builder)
    commercial_jet_airplane = director.construct_airplane()
    print(commercial_jet_airplane)

    private_jet_builder = PrivateJetAirplaneBuilder()
    director = Director(private_jet_builder)
    private_jet_airplane = director.construct_airplane()
    print(private_jet_airplane)

if __name__ == "__main__":
    main()
```

### `main.py` execution output:

```
Doing build_fuselage
Doing attach_wings
Doing install_interior for CommercialJet
Doing test_flight for CommercialJet
Airplane of type CommercialJet with fuselage Fuselage, wings Wings, wheels Wheels.
Doing build_fuselage
Doing attach_wings
Doing install_interior for PrivateJet
Doing test_flight for PrivateJet
Airplane of type PrivateJet with fuselage Fuselage, wings Wings, wheels Wheels.
```
