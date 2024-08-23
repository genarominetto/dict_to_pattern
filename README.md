# Dict to Pattern

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/genarominetto/dict_to_pattern/blob/main/main.ipynb)

This is a scaffolder (code project generator) solution to create complete python template programs with tests from simple dictionaries. The idea is to create a scaffolder for each design pattern in the book **"[Design Patterns](https://en.wikipedia.org/wiki/Design_Patterns)"**. The project currently includes two scaffolders:

1. [**Builder Scaffolder**](scaffolders/builder/): Constructs programs that align with the Builder design pattern.
2. [**Facade Scaffolder**](scaffolders/facade/): Constructs programs that align with the Facade design pattern.

## TO GET STARTED, **PRESS** THE "OPEN IN COLAB" BUTTON AND **RUN** EVERY CELL.

- After the tests pass, the generated projects will automatically download to your PC.  
- Once you are familiar with the notebook, edit the example `project_structure` dict and rerun the cell to generate your own program skeletons.  
- If you want your new project to be a submodule of an existing project, update the `root_module` parameter (e.g., `root_module = "module.sub_module"`) to specify the desired module hierarchy.



## Project Structure

```
.
├── scaffolders
│   ├── builder
│   │   └── [Builder-specific modules and scripts]
│   └── facade
│       └── [Facade-specific modules and scripts]
├── jupyter.py
└── main.ipynb
```



