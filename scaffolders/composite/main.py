from modules.helpers.component_file_builder.builders.abstract_component_file_builder import AbstractComponentFileBuilder
from modules.helpers.component_file_builder.builders.composite_component_file_builder import CompositeComponentFileBuilder
from modules.helpers.component_file_builder.builders.abstract_leaf_component_file_builder import AbstractLeafComponentFileBuilder
from modules.helpers.component_file_builder.director import Director

def main():
    abstract_builder = AbstractComponentFileBuilder()
    director = Director(abstract_builder)
    abstract_component_file = director.construct_component_file()
    print(abstract_component_file)

    composite_builder = CompositeComponentFileBuilder()
    director = Director(composite_builder)
    composite_component_file = director.construct_component_file()
    print(composite_component_file)

    abstract_leaf_builder = AbstractLeafComponentFileBuilder()
    director = Director(abstract_leaf_builder)
    abstract_leaf_component_file = director.construct_component_file()
    print(abstract_leaf_component_file)

if __name__ == "__main__":
    main()
