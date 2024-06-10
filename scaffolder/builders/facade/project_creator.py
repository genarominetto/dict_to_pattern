# project_creator.py

from modules.main_file_creator import MainFileCreator
from modules.branch_file_creator import BranchFileCreator
from modules.leaf_file_creator import LeafFileCreator
from modules.test_file_creator import TestFileCreator
from modules.simple_file_creator import SimpleFileCreator

class ProjectCreator:
    def __init__(self, project_name, project_structure):
        self.project_name = project_name
        self.project_structure = project_structure

    def create_project(self):
        pass

if __name__ == "__main__":
    project_structure = {
        "Car": {
            "Engine": {
                "Cylinders": {},
                "Pistons": {}
            },
            "Chassis": {}
        }
    }

    creator = ProjectCreator("FacadeProject", project_structure)
    creator.create_project()
