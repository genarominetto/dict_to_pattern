import os
import shutil
from modules.abstract_builder_file_creator import AbstractBuilderFileCreator
from modules.concrete_builder_file_creator import ConcreteBuilderFileCreator
from modules.director_file_creator import DirectorFileCreator
from modules.main_file_creator import MainFileCreator
from modules.product_file_creator import ProductFileCreator
from modules.product_part_file_creator import ProductPartFileCreator
from modules.test_file_creator import TestFileCreator
from modules.simple_file_creator import SimpleFileCreator

class StructureHelper:
    def __init__(self, project_structure, root_module):
        self.project_structure = project_structure
        self.root_module = root_module

    def _convert_to_snake_case(self, name):
        # Convert CamelCase to snake_case
        return ''.join(['_' + c.lower() if c.isupper() else c for c in name]).lstrip('_')

    def create_directory_structure(self, root_path):
        # Extract main components from project_structure
        product_name = self.project_structure["product"]

        # Convert names to snake_case
        product_name_snake = self._convert_to_snake_case(product_name)

        # Define dynamic directory names based on the project structure
        builder_root_dir = os.path.join(root_path, f"{product_name_snake}_builder")
        product_root_dir = os.path.join(builder_root_dir, "product")
        parts_dir = os.path.join(product_root_dir, f"{product_name_snake}_parts")
        builder_abstract_dir = os.path.join(builder_root_dir, "builders", "abstract")
        builder_concrete_dir = os.path.join(builder_root_dir, "builders")
        test_root_dir = os.path.join(root_path, "tests")

        # Create directories dynamically
        os.makedirs(builder_abstract_dir, exist_ok=True)
        os.makedirs(parts_dir, exist_ok=True)
        os.makedirs(builder_concrete_dir, exist_ok=True)
        os.makedirs(test_root_dir, exist_ok=True)

        return builder_concrete_dir, builder_root_dir, product_root_dir, parts_dir, test_root_dir

    def create_filenames(self):
        # Generate filenames dynamically based on the project structure
        filenames = {}
        product_name = self.project_structure["product"]
        product_name_snake = self._convert_to_snake_case(product_name)
        filenames['abstract_builder'] = f"{product_name_snake}_builder.py"
        filenames['product'] = f"{product_name_snake}.py"
        filenames['director'] = "director.py"
        filenames['main'] = "main.py"
        filenames['test_files'] = [f"test_{self._convert_to_snake_case(type_name)}_{product_name_snake}.py" for type_name in self.project_structure["types"]]
        filenames['concrete_builders'] = [f"{self._convert_to_snake_case(type_name)}_{product_name_snake}_builder.py" for type_name in self.project_structure["types"]]
        filenames['parts'] = [f"{self._convert_to_snake_case(part_name)}.py" for part_name in self.project_structure["parts"]]
        return filenames

class BuilderProjectCreator:
    def __init__(self, project_name, project_structure, root_module):
        self.project_name = project_name
        self.project_structure = project_structure
        self.root_module = root_module
        self.helper = StructureHelper(project_structure, root_module)

    def create_project(self):
        # Delete the project directory if it exists
        if os.path.exists(self.project_name):
            shutil.rmtree(self.project_name)

        # Create the project root directory
        os.makedirs(self.project_name, exist_ok=True)

        # Create the complete directory structure
        builder_concrete_dir, builder_root_dir, product_root_dir, parts_dir, test_root_dir = self.helper.create_directory_structure(self.project_name)

        # Create __init__.py files in all directories
        SimpleFileCreator(os.path.join(builder_root_dir, "__init__.py")).create_simple_file("")
        SimpleFileCreator(os.path.join(product_root_dir, "__init__.py")).create_simple_file("")
        SimpleFileCreator(os.path.join(parts_dir, "__init__.py")).create_simple_file("")
        SimpleFileCreator(os.path.join(builder_concrete_dir, "__init__.py")).create_simple_file("")
        SimpleFileCreator(os.path.join(test_root_dir, "__init__.py")).create_simple_file("")

        # Create the pytest.ini file
        pytest_ini_path = os.path.join(self.project_name, "pytest.ini")
        SimpleFileCreator(pytest_ini_path).create_simple_file("[pytest]\npythonpath = .\n")

        # Create the abstract builder file
        filenames = self.helper.create_filenames()
        abstract_builder_filename = os.path.join(self.project_name, "vacation_house_builder", "builders", "abstract", filenames['abstract_builder'])
        abstract_builder_creator = AbstractBuilderFileCreator(abstract_builder_filename, self.root_module)
        abstract_builder_creator.create_abstract_builder_file(self.project_structure)

        # Create concrete builder files
        for type_name in self.project_structure["types"]:
            concrete_builder_filename = os.path.join(builder_concrete_dir, filenames['concrete_builders'][self.project_structure["types"].index(type_name)])
            concrete_builder_creator = ConcreteBuilderFileCreator(concrete_builder_filename, self.root_module)
            concrete_builder_creator.create_concrete_builder_file(type_name, self.project_structure)

        # Create the director file
        director_filename = os.path.join(builder_root_dir, filenames['director'])
        director_creator = DirectorFileCreator(director_filename, self.root_module)
        director_creator.create_director_file(self.project_structure)

        # Create the product file
        product_filename = os.path.join(product_root_dir, filenames['product'])
        product_creator = ProductFileCreator(product_filename, self.root_module)
        product_creator.create_product_file(self.project_structure)

        # Create product part files
        for part_name in self.project_structure["parts"]:
            part_filename = os.path.join(parts_dir, filenames['parts'][self.project_structure["parts"].index(part_name)])
            part_creator = ProductPartFileCreator(part_filename, self.root_module)
            part_creator.create_product_part_file(part_name)

        # Create test files
        for type_name in self.project_structure["types"]:
            test_filename = os.path.join(test_root_dir, filenames['test_files'][self.project_structure["types"].index(type_name)])
            test_creator = TestFileCreator(test_filename, self.root_module)
            test_creator.create_test_file(type_name, self.project_structure)

        # Create the main file
        main_filename = os.path.join(self.project_name, filenames['main'])
        main_creator = MainFileCreator(main_filename, self.root_module)
        main_creator.create_main_file(self.project_structure)

if __name__ == "__main__":
    project_structure = {
        "product": "VacationHouse",
        "types": ["OceanBeach", "RockMountain"],
        "parts": ["FoundationBase", "InteriorDesign"],
        "parent_steps": ["prepare_the_foundation", "inspect_foundation"],
        "child_steps": ["build_the_structure", "finalize_details"]
    }

    root_module = "dir_a.dir_b"  # Define the root module
    creator = BuilderProjectCreator("BuilderProject", project_structure, root_module)
    creator.create_project()
