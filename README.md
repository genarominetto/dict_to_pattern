# Dict to Pattern

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/genarominetto/dict_to_pattern/blob/main/main.ipynb)

This is a scaffolder (code project generator) solution to create complete python template programs with tests from simple dictionaries. The idea is to create one scaffolder for each design pattern in the book **"[Design Patterns](https://en.wikipedia.org/wiki/Design_Patterns)"**. The project currently includes three scaffolders:

1. [**Builder Scaffolder**](scaffolders/builder/): Creates programs that align with the Builder design pattern. Use it to separate the construction of a complex object from its representation.
2. [**Facade Scaffolder**](scaffolders/facade/): Creates programs that align with the Facade design pattern. Use it to provide a unified interface to a set of interfaces in a subsystem.
3. [**State Scaffolder**](scaffolders/state/): Creates programs that align with the State design pattern. Allows an object to alter its behavior when its internal state changes.

## [Open in colab](https://colab.research.google.com/github/genarominetto/dict_to_pattern/blob/main/main.ipynb) and run every cell to get started.

- After the tests pass, the generated projects will automatically download to your PC.  
- Once you are familiar with the notebook, edit the example `project_structure` dict and rerun the cell to generate your own program templates.  
- If you want your new project to be a submodule of an existing project, update the `root_module` parameter (e.g., `root_module = "my_module.my_sub_module"`) to specify the desired module hierarchy.




