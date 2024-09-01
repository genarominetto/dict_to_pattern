# State Scaffolder

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/genarominetto/dict_to_pattern/blob/main/main.ipynb)


### State Pattern

- **Definition:** Allows an object to alter its behavior when its internal state changes.
- **Aspects that Vary:** States of an object.
- **Participants:** Context, State, ConcreteState.

## Overview

The **State Scaffolder** creates programs that align with the State design pattern. Define the project structure using the dict `project_structure` to create classes, methods, and tests. Modify the dict values to customize the program as needed.

## How to Use

- Define `project_name`, `project_structure`, and `root_module`.
- Customize `project_structure` to set desired classes and methods.

## Example Input:

```python
project_structure = {
    "context": "TrafficLight",
    "default_state": "Red",
    "state_transitions": {
        "Red": ["Yellow"],
        "Green": ["Yellow"],
        "Yellow": ["Red", "Green"]
    },
    "properties": [
        "timer_duration",
        "is_operational"
    ],
    "methods": [
        "adjust_brightness",
        "switch_to_backup_power"
    ]
}
```

## Example Output:

### Generated Project Structure:

```
.
├── traffic_light
│   ├── states
│   │   ├── abstract
│   │   │   └── state.py
│   │   ├── green_state.py
│   │   ├── red_state.py
│   │   └── yellow_state.py
│   ├── tests
│   │   ├── test_green_state.py
│   │   ├── test_red_state.py
│   │   └── test_yellow_state.py
│   └── traffic_light.py
├── main.py
└── pytest.ini
```

### Generated `main.py` file:

```python
from traffic_light.traffic_light import TrafficLight

if __name__ == "__main__":
    traffic_light = TrafficLight()  # Initial state: red
    traffic_light.set_state_to_yellow()
    traffic_light.set_state_to_yellow()
    traffic_light.set_state_to_red()
    traffic_light.set_state_to_green()
    traffic_light.adjust_brightness()
    traffic_light.switch_to_backup_power()
    traffic_light.report_status()
```

### `main.py` execution output:

```
Switching from Red State to Yellow state.
Already in Yellow State.
Switching from Yellow State to Red state.
Transition from Red State to Green state is not allowed.
State: Red State
- Timer duration: None
- Is operational: None
```
