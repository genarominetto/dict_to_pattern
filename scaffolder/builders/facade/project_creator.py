from modules.main_file_creator import MainFileCreator
from modules.branch_file_creator import BranchFileCreator
from modules.leaf_file_creator import LeafFileCreator
from modules.test_file_creator import TestFileCreator
from modules.simple_file_creator import SimpleFileCreator
import os
class StructureHelper:
    def __init__(self, project_structure):
        self.project_structure = project_structure

    def get_structure_info(self):
        branch_files = []
        leaf_files = []
        test_info = {}

        root_class = self._extract_root_class(self.project_structure)
        self._process_structure(self.project_structure[root_class], root_class, 'car', branch_files, leaf_files)

        leaf_ladders = self._get_leaf_ladders(self.project_structure[root_class], root_class)
        test_info = {
            "file_path": f"tests/test_{root_class.lower()}.py",
            "root_class": root_class,
            "leaf_ladders": leaf_ladders
        }

        return branch_files, leaf_files, test_info

    def _process_structure(self, structure, class_name, current_path, branch_files, leaf_files):
        if structure:
            subcomponents = sorted(list(structure.keys()))
            branch_file_path = f"{current_path}/{class_name.lower()}.py"
            branch_files.append({
                "class_name": class_name,
                "subcomponents": subcomponents,
                "file_path": branch_file_path
            })
            for subcomponent in subcomponents:
                if class_name.lower() == "car":
                    new_path = f"{current_path}/car_modules"
                elif class_name.lower() == "engine":
                    new_path = f"{current_path}/engine_modules"
                else:
                    new_path = current_path
                self._process_structure(structure[subcomponent], subcomponent, new_path, branch_files, leaf_files)
        else:
            leaf_files.append({
                "class_name": class_name,
                "file_path": f"{current_path}/{class_name.lower()}.py"
            })

    def _get_leaf_ladders(self, structure, root_class):
        leaf_ladders = []
        self._traverse_structure(structure, [root_class.lower()], leaf_ladders)
        return leaf_ladders

    def _traverse_structure(self, structure, ladder, leaf_ladders):
        if not structure:
            leaf_ladders.append(ladder)
            return
        for key, value in sorted(structure.items()):
            self._traverse_structure(value, ladder + [key.lower()], leaf_ladders)

    def _extract_root_class(self, structure):
        return next(iter(structure))

class ProjectCreator:
    def __init__(self, project_name, project_structure):
        self.project_name = project_name
        self.project_structure = project_structure
        self.helper = StructureHelper(project_structure)

    def create_project(self):
        self._create_directory(self.project_name)
        self._create_main_file()
        self._create_root_init_file()
        self._create_pytest_ini()
        self._create_tests_directory()

        branch_files, leaf_files, test_info = self.helper.get_structure_info()
        self._create_branch_files(branch_files)
        self._create_leaf_files(leaf_files)
        self._create_test_file(test_info)

    def _create_directory(self, path):
        os.makedirs(path, exist_ok=True)

    def _create_main_file(self):
        main_creator = MainFileCreator(f"{self.project_name}/main.py")
        main_creator.create_main_file(self.project_structure)

    def _create_root_init_file(self):
        init_creator = SimpleFileCreator(f"{self.project_name}/__init__.py")
        init_creator.create_simple_file('')

    def _create_pytest_ini(self):
        with open(f"{self.project_name}/pytest.ini", 'w') as pytest_file:
            pytest_file.write("[pytest]\n")

    def _create_tests_directory(self):
        tests_dir = f"{self.project_name}/tests"
        self._create_directory(tests_dir)
        init_creator = SimpleFileCreator(f"{tests_dir}/__init__.py")
        init_creator.create_simple_file('')

    def _create_branch_files(self, branch_files):
        for branch in branch_files:
            dir_path = os.path.dirname(f"{self.project_name}/{branch['file_path']}")
            self._create_directory(dir_path)
            branch_creator = BranchFileCreator(f"{self.project_name}/{branch['file_path']}")
            branch_creator.create_branch_file(branch['class_name'], branch['subcomponents'])
            init_creator = SimpleFileCreator(f"{dir_path}/__init__.py")
            init_creator.create_simple_file('')

    def _create_leaf_files(self, leaf_files):
        for leaf in leaf_files:
            dir_path = os.path.dirname(f"{self.project_name}/{leaf['file_path']}")
            self._create_directory(dir_path)
            leaf_creator = LeafFileCreator(f"{self.project_name}/{leaf['file_path']}")
            leaf_creator.create_leaf_file(leaf['class_name'])
            init_creator = SimpleFileCreator(f"{dir_path}/__init__.py")
            init_creator.create_simple_file('')

    def _create_test_file(self, test_info):
        test_creator = TestFileCreator(f"{self.project_name}/{test_info['file_path']}")
        test_creator.create_test_file(test_info['root_class'], test_info['leaf_ladders'])

if __name__ == "__main__":
    project_structure = {
        "Car": {
            "Engine": {
                "Cylinders": {},
                "Pistons": {
                    "PistonRings": {},
                    "PistonHead": {}
                },
            },
            "Chassis": {}
        }
    }

    creator = ProjectCreator("FacadeProjectl", project_structure)
    creator.create_project()
