import os
import shutil
from modules.abstract_builder_file_creator import AbstractBuilderFileCreator

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
        types = self.project_structure["types"]
        parts = self.project_structure["parts"]

        # Convert names to snake_case
        product_name_snake = self._convert_to_snake_case(product_name)

        # Define dynamic directory names based on the project structure
        builder_root_dir = os.path.join(root_path, f"{product_name_snake}_builder")
        product_root_dir = os.path.join(builder_root_dir, "product")
        parts_dir = os.path.join(product_root_dir, f"{product_name_snake}_parts")
        builder_dir = os.path.join(builder_root_dir, "builders", "abstract")
        test_root_dir = os.path.join(root_path, "tests")

        # Create directories dynamically
        os.makedirs(builder_dir, exist_ok=True)
        os.makedirs(parts_dir, exist_ok=True)
        os.makedirs(test_root_dir, exist_ok=True)

        # Create placeholders for concrete builder files
        for type_name in types:
            os.makedirs(os.path.join(builder_root_dir, "builders"), exist_ok=True)

        # Create placeholder for product-related files
        os.makedirs(product_root_dir, exist_ok=True)

    def create_filenames(self):
        # Generate filenames dynamically based on the project structure
        filenames = {}
        product_name = self.project_structure["product"]
        product_name_snake = self._convert_to_snake_case(product_name)
        filenames['abstract_builder'] = f"{product_name_snake}_builder.py"
        filenames['product'] = f"{product_name_snake}.py"
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
        self.helper.create_directory_structure(self.project_name)

        # Create the abstract builder file
        filenames = self.helper.create_filenames()
        abstract_builder_filename = os.path.join(self.project_name, "vacation_house_builder", "builders", "abstract", filenames['abstract_builder'])
        abstract_builder_creator = AbstractBuilderFileCreator(abstract_builder_filename, self.root_module)
        abstract_builder_creator.create_abstract_builder_file(self.project_structure)


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
