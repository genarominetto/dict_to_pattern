import os
import shutil

class StructureHelper:
    def __init__(self, project_structure):
        self.project_structure = project_structure
        self.root_module = root_module

class BuilderProjectCreator:
    def __init__(self, project_name, project_structure):
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
