import os
import shutil

class StructureHelper:
    def __init__(self, project_structure):
        self.project_structure = project_structure

class BuilderProjectCreator:
    def __init__(self, project_name, project_structure):
        self.project_name = project_name
        self.project_structure = project_structure
        self.helper = StructureHelper(project_structure)

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

    creator = BuilderProjectCreator("BuilderProject", project_structure)
    creator.create_project()
