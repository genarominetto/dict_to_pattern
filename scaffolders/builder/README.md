# Builder Scaffolder

## Overview
The **Builder Scaffolder** generates a Python project template using the Builder design pattern. Define the project structure using a dictionary to create classes, methods, and tests. Modify the dictionary values to customize the program as needed.

## How to Use

1. **Set Up Project**:
    - Define `project_name`, `project_structure`, and `root_module`.
    - Customize `project_structure` to set desired classes and methods:
        - `product`, `types`, and `parts` represent Python classes.
        - `parent_steps` and `child_steps` represent methods within builder classes.

    Example:

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

2. **Generate Project**:
    - Run the notebook code to create the project.
    - Generated directories, classes, and tests follow the dictionary structure.

3. **Run Tests**:
    - Use `pytest` to verify the generated project.

4. **Download Generated Code**:
    - After tests pass, download the compressed project.

## Project Structure

```
.
├── airplane_builder
│   ├── builders
│   ├── product
│   └── director.py
├── tests
├── main.py
└── pytest.ini
```
