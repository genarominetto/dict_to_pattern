project_structure = {
    "product": "VacationHouse",
    "types": ["OceanBeach", "RockMountain"],
    "abstract_parts": ["FoundationBase", "StructureBase"],
    "concrete_parts": ["InteriorDesign", "OutdoorDesign"]
}




project/
│
├── builders/
│   ├── abstract_builder/
│   │   └── vacation_house_builder.py
│   ├── ocean_beach_vacation_house_builder.py
│   └── rock_mountain_vacation_house_builder.py
│
├── product/
│   └── vacation_house.py
│
├── parts/
│   ├── foundation_base.py
│   ├── structure_base.py
│   ├── interior_design.py
│   └── outdoor_design.py
│
├── director/
│   └── director.py
│
└── tests/
    ├── test_ocean_beach_vacation_house.py
    └── test_rock_mountain_vacation_house.py
