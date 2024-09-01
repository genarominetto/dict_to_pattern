# facade_project_creator.py

from modules.main_file_creator import MainFileCreator
from modules.branch_file_creator import BranchFileCreator
from modules.leaf_file_creator import LeafFileCreator
from modules.test_file_creator import TestFileCreator
from modules.simple_file_creator import SimpleFileCreator
import os
import shutil

class StructureHelper:
    def __init__(self, project_structure, root_module=None):
        self.project_structure = project_structure
        self.root_module = root_module

    def get_structure_info(self):
        branch_files = []
        leaf_files = []
        test_info = {}

        for root_class in self.project_structure:
            self._process_structure(self.project_structure[root_class], root_class, root_class.lower(), [], branch_files, leaf_files)

            leaf_ladders = self._get_leaf_ladders(self.project_structure[root_class], root_class)
            test_info[root_class] = {
                "file_path": f"tests/test_{root_class.lower()}.py",
                "root_class": root_class,
                "leaf_ladders": leaf_ladders
            }

        return branch_files, leaf_files, test_info

    def _process_structure(self, structure, class_name, current_path, ladder, branch_files, leaf_files):
        new_ladder = ladder + [class_name]
        if structure:
            subcomponents = sorted(list(structure.keys()))
            branch_file_path = f"{current_path}/{class_name.lower()}.py"
            subcomponent_ladders = [new_ladder + [sub] for sub in subcomponents]
            branch_files.append({
                "class_name": class_name,
                "subcomponents_ladders": subcomponent_ladders,
                "file_path": branch_file_path
            })
            for subcomponent in subcomponents:
                new_path = f"{current_path}/{class_name.lower()}_modules"
                self._process_structure(structure[subcomponent], subcomponent, new_path, new_ladder, branch_files, leaf_files)
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

class FacadeProjectCreator:
    def __init__(self, project_name, project_structure, root_module=None):
        self.project_name = project_name
        self.project_structure = project_structure
        self.root_module = root_module
        self.helper = StructureHelper(project_structure, root_module)

    def create_project(self):
        # Delete the project directory if it exists
        if os.path.exists(self.project_name):
            shutil.rmtree(self.project_name)

        # Create the project root directory
        self._create_directory(self.project_name)

        # Create main.py and pytest.ini in the project root directory
        self._create_main_file()
        self._create_pytest_ini()

        # Create root module directories for the rest of the files
        root_path = self._create_root_module_directories()

        self._create_directory(root_path)
        self._create_root_init_file(root_path)
        self._create_tests_directory(root_path)

        branch_files, leaf_files, test_info = self.helper.get_structure_info()
        self._create_branch_files(root_path, branch_files)
        self._create_leaf_files(root_path, leaf_files)
        self._create_test_files(root_path, test_info)

    def _create_root_module_directories(self):
        if self.root_module:
            parts = self.root_module.split('.')
            root_path = os.path.join(self.project_name, *parts)
            os.makedirs(root_path, exist_ok=True)
            return root_path
        else:
            return self.project_name

    def _create_directory(self, path):
        os.makedirs(path, exist_ok=True)

    def _create_main_file(self):
        main_creator = MainFileCreator(f"{self.project_name}/main.py", self.root_module)
        main_creator.create_main_file(self.project_structure)

    def _create_root_init_file(self, root_path):
        init_creator = SimpleFileCreator(f"{root_path}/__init__.py")
        init_creator.create_simple_file('')

    def _create_pytest_ini(self):
        with open(f"{self.project_name}/pytest.ini", 'w') as pytest_file:
            pytest_file.write("[pytest]\npythonpath = .\n")

    def _create_tests_directory(self, root_path):
        tests_dir = f"{root_path}/tests"
        self._create_directory(tests_dir)
        init_creator = SimpleFileCreator(f"{tests_dir}/__init__.py")
        init_creator.create_simple_file('')

    def _create_branch_files(self, root_path, branch_files):
        for branch in branch_files:
            dir_path = os.path.dirname(f"{root_path}/{branch['file_path']}")
            self._create_directory(dir_path)
            branch_creator = BranchFileCreator(f"{root_path}/{branch['file_path']}", self.root_module)
            branch_creator.create_branch_file(branch['class_name'], branch['subcomponents_ladders'])
            init_creator = SimpleFileCreator(f"{dir_path}/__init__.py")
            init_creator.create_simple_file('')

    def _create_leaf_files(self, root_path, leaf_files):
        for leaf in leaf_files:
            dir_path = os.path.dirname(f"{root_path}/{leaf['file_path']}")
            self._create_directory(dir_path)
            leaf_creator = LeafFileCreator(f"{root_path}/{leaf['file_path']}", self.root_module)
            leaf_creator.create_leaf_file(leaf['class_name'])
            init_creator = SimpleFileCreator(f"{dir_path}/__init__.py")
            init_creator.create_simple_file('')

    def _create_test_files(self, root_path, test_info):
        for root_class, info in test_info.items():
            test_creator = TestFileCreator(f"{root_path}/{info['file_path']}", self.root_module)
            test_creator.create_test_file(info['root_class'], info['leaf_ladders'])


