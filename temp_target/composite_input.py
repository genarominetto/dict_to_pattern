project_structure = {
    "component" : "Graphic",
    "composite" : "Group",
    "leaves" : ["Circle", "Square"],
    "leaf_properties" : {
        "size" : 3,
        "is_active" : True
    }
}





.
├── component
│   ├── abstract
│   │   ├── graphic_modules
│   │   │   ├── data_loader.py
│   │   │   └── graphic_validator.py
│   │   └── graphic.py
│   ├── components
│   │   ├── composite
│   │   │   └── group.py
│   │   └── leafs
│   │       ├── abstract
│   │       │   └── leaf.py
│   │       ├── circle.py
│   │       └── square.py
│   └── tests
│       ├── test_circle.py
│       └── test_square.py
├── main.py
└── pytest.ini

8 directories, 11 files




