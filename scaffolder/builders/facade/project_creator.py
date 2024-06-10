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
        # Create root directory
        self._create_directory(self.project_name)
        # Create main.py file
        main_creator = MainFileCreator(f"{self.project_name}/main.py")
        main_creator.create_main_file(self.project_structure)
        # Create root __init__.py file
        init_creator = SimpleFileCreator(f"{self.project_name}/__init__.py")
        init_creator.create_simple_file('')
        # Create pytest.ini file
        with open(f"{self.project_name}/pytest.ini", 'w') as pytest_file:
            pytest_file.write("[pytest]\n")
        # Create tests directory and test file
        tests_dir = f"{self.project_name}/tests"
        self._create_directory(tests_dir)
        init_creator = SimpleFileCreator(f"{tests_dir}/__init__.py")
        init_creator.create_simple_file('')
        root_class = self._extract_root_class(self.project_structure)
        subcomponents = self._extract_subcomponents(self.project_structure[root_class])
        test_creator = TestFileCreator(f"{tests_dir}/test_{root_class.lower()}.py")
        test_creator.create_test_file(root_class, subcomponents)
        # Create project structure
        self._create_structure(self.project_structure, self.project_name)

    def _create_structure(self, structure, parent_path):
        for name, sub_structure in structure.items():
            current_path = f"{parent_path}/{name.lower()}"
            self._create_directory(current_path)
            # Create branch files for intermediate directories
            if sub_structure:
                subcomponents = self._extract_subcomponents(sub_structure)
                branch_creator = BranchFileCreator(f"{current_path}/{name.lower()}.py")
                branch_creator.create_branch_file(name, subcomponents)
            else:
                leaf_creator = LeafFileCreator(f"{current_path}/{name.lower()}.py")
                leaf_creator.create_leaf_file(name)
            # Create __init__.py file in each directory
            init_creator = SimpleFileCreator(f"{current_path}/__init__.py")
            init_creator.create_simple_file('')
            # Recursively create sub-structure
            if sub_structure:
                self._create_structure(sub_structure, current_path)

    def _create_directory(self, path):
        import os
        os.makedirs(path, exist_ok=True)

    def _extract_root_class(self, structure):
        return next(iter(structure))

    def _extract_subcomponents(self, structure, prefix=''):
        subcomponents = []
        for key, value in structure.items():
            current_prefix = f"{prefix}.{key.lower()}" if prefix else key.lower()
            subcomponents.append(current_prefix)
        return subcomponents

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
