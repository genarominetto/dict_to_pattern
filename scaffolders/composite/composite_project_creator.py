import os
import shutil
from modules.helpers.helper import Helper
from modules.abstract_component_file_creator import AbstractComponentFileCreator
from modules.abstract_leaf_file_creator import AbstractLeafFileCreator
from modules.composite_file_creator import CompositeFileCreator
from modules.concrete_leaf_file_creator import ConcreteLeafFileCreator
from modules.data_loader_file_creator import DataLoaderFileCreator
from modules.validator_file_creator import ValidatorFileCreator
from modules.main_file_creator import MainFileCreator
from modules.simple_file_creator import SimpleFileCreator
from modules.test_file_creator import TestFileCreator

class StructureHelper:
    def __init__(self, project_structure):
        self.project_structure = project_structure

    def create_directory_structure(self, root_path):
        # Extract names from project_structure
        component_name = self.project_structure["component"]
        composite_name = self.project_structure["composite"]

        # Convert names to snake_case
        component_name_snake = Helper.convert_to_snake_case(component_name)
        composite_name_snake = Helper.convert_to_snake_case(composite_name)

        # Define directories based on the component name
        component_root_dir = os.path.join(root_path, component_name_snake)
        abstract_dir = os.path.join(component_root_dir, 'abstract')
        abstract_modules_dir = os.path.join(abstract_dir, f'{component_name_snake}_modules')
        components_dir = os.path.join(component_root_dir, 'components')
        composite_dir = os.path.join(components_dir, 'composite')
        leaves_dir = os.path.join(components_dir, 'leaves')
        abstract_leaf_dir = os.path.join(leaves_dir, 'abstract')
        tests_dir = os.path.join(component_root_dir, 'tests')

        # Create directories dynamically
        os.makedirs(abstract_modules_dir, exist_ok=True)
        os.makedirs(composite_dir, exist_ok=True)
        os.makedirs(abstract_leaf_dir, exist_ok=True)
        os.makedirs(leaves_dir, exist_ok=True)
        os.makedirs(tests_dir, exist_ok=True)

        return {
            'component_root_dir': component_root_dir,
            'abstract_dir': abstract_dir,
            'abstract_modules_dir': abstract_modules_dir,
            'components_dir': components_dir,
            'composite_dir': composite_dir,
            'leaves_dir': leaves_dir,
            'abstract_leaf_dir': abstract_leaf_dir,
            'tests_dir': tests_dir
        }

class CompositeProjectCreator:
    def __init__(self, project_name, project_structure, root_module):
        self.project_name = project_name
        self.project_structure = project_structure
        self.structure_helper = StructureHelper(project_structure)
        self.root_module = root_module  # Add root_module attribute

    def create_project(self):
        # Delete the project directory if it exists
        if os.path.exists(self.project_name):
            shutil.rmtree(self.project_name)

        # Create the project root directory
        os.makedirs(self.project_name, exist_ok=True)

        # Create the complete directory structure
        dirs = self.structure_helper.create_directory_structure(self.project_name)

        # Create __init__.py files in necessary directories using SimpleFileCreator
        for dir_path in dirs.values():
            init_file = os.path.join(dir_path, '__init__.py')
            os.makedirs(dir_path, exist_ok=True)
            simple_creator = SimpleFileCreator(init_file)
            simple_creator.create_simple_file("")

        # Create the pytest.ini file using SimpleFileCreator
        pytest_ini_path = os.path.join(self.project_name, 'pytest.ini')
        simple_creator = SimpleFileCreator(pytest_ini_path)
        simple_creator.create_simple_file("[pytest]\npythonpath = .\n")

        # Create the abstract component file using AbstractComponentFileCreator
        abstract_component_filename = os.path.join(
            dirs['abstract_dir'],
            f"{Helper.convert_to_snake_case(self.project_structure['component'])}.py"
        )
        abstract_creator = AbstractComponentFileCreator(abstract_component_filename, self.root_module)
        abstract_creator.create_abstract_component_file(self.project_structure)

        # Create the composite component file using CompositeFileCreator
        composite_component_filename = os.path.join(
            dirs['composite_dir'],
            f"{Helper.convert_to_snake_case(self.project_structure['composite'])}.py"
        )
        composite_creator = CompositeFileCreator(composite_component_filename, self.root_module)
        composite_creator.create_composite_file(self.project_structure)

        # Create the abstract leaf component file using AbstractLeafFileCreator
        abstract_leaf_filename = os.path.join(dirs['abstract_leaf_dir'], 'leaf.py')
        abstract_leaf_creator = AbstractLeafFileCreator(abstract_leaf_filename, self.root_module)
        abstract_leaf_creator.create_abstract_leaf_file(self.project_structure)

        # Create the data loader file using DataLoaderFileCreator
        data_loader_filename = os.path.join(
            dirs['abstract_modules_dir'],
            'data_loader.py'
        )
        data_loader_creator = DataLoaderFileCreator(data_loader_filename, self.root_module)
        data_loader_creator.create_data_loader_file(self.project_structure)

        # Create the validator file using ValidatorFileCreator
        validator_filename = os.path.join(
            dirs['abstract_modules_dir'],
            f"{Helper.convert_to_snake_case(self.project_structure['component'])}_validator.py"
        )
        validator_creator = ValidatorFileCreator(validator_filename, self.root_module)
        validator_creator.create_validator_file(self.project_structure)

        # Create concrete leaf files using ConcreteLeafFileCreator
        for leaf in self.project_structure['leaves']:
            leaf_filename = os.path.join(
                dirs['leaves_dir'],
                f"{Helper.convert_to_snake_case(leaf)}.py"
            )
            leaf_creator = ConcreteLeafFileCreator(leaf_filename, self.root_module)
            leaf_creator.create_concrete_leaf_file(self.project_structure)

        # Create test files for leaves using TestFileCreator
        for leaf in self.project_structure['leaves']:
            test_filename = os.path.join(
                dirs['tests_dir'],
                f"test_{Helper.convert_to_snake_case(leaf)}.py"
            )
            test_creator = TestFileCreator(test_filename, self.root_module)
            test_creator.create_test_file(self.project_structure)

        # Create main.py file using MainFileCreator
        main_filename = os.path.join(self.project_name, 'main.py')
        main_creator = MainFileCreator(main_filename, self.root_module)
        main_creator.create_main_file(self.project_structure)

if __name__ == "__main__":
    project_structure = {
        "component": "Graphic",
        "composite": "Group",
        "leaves": ["Circle", "Square"],
        "leaf_properties": {
            "size": 3,
            "is_active": True
        }
    }

    # Pass "dir.sub_dir" as the root module as specified
    creator = CompositeProjectCreator("CompositeProject", project_structure, "dir.sub_dir")
    creator.create_project()
