project_structure = {
    "context": "LightSwitch",
    "default_state": "Off",
    "state_transitions": {
        "On": [],
        "Off": ["On"]
    },
    "properties": [
        "energy_saving_mode",
        "is_active"
    ],
    "methods": [
        "additional_operation",
        "another_additional_operation"
    ]
}





.
├── light_switch
│   ├── light_switch.py
│   ├── states
│   │   ├── abstract
│   │   │   └── state.py
│   │   ├── off_state.py
│   │   └── on_state.py
│   └── tests
│       ├── test_off_state.py
│       └── test_on_state.py
├── main.py
└── pytest.ini


