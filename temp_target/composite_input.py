project_structure = {
    "component" : "graphic",
    "composite" : "group",
    "leaves" : ["circle", "square"],
    "leaf_properties" : {
        "str" : [],
        "int" : [],
        "float" : ["size"],
        "bool" : ["active"]
    }
}





.
├── graphic_drawing
│   ├── base
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



