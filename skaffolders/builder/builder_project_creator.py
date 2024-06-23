from modules.abstract_builder_file_creator import AbstractBuilderFileCreator
from modules.concrete_builder_file_creator import ConcreteBuilderFileCreator
from modules.director_file_creator import DirectorFileCreator
from modules.main_file_creator import MainFileCreator
from modules.product_file_creator import ProductFileCreator
from modules.simple_file_creator import SimpleFileCreator
from modules.test_file_creator import TestFileCreator
import os
import shutil

class StructureHelper:
    def __init__(self, project_structure, root_module):
        self.project_structure = project_structure
        self.root_module = root_module

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

if __name__ == "__main__":
    project_structure = {
        "product": "house",
        "types": ["modern", "victorian"],
        "abstract_parts": ["foundation", "structure"],
        "concrete_parts": ["roof", "interior"]
    }

    root_module = "dir_a.dir_b"  # Define the root module
    creator = BuilderProjectCreator("BuilderProject", project_structure, root_module)
    creator.create_project()
