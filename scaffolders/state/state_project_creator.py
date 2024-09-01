import os
import shutil
from modules.abstract_state_file_creator import AbstractStateFileCreator
from modules.concrete_state_file_creator import ConcreteStateFileCreator
from modules.context_file_creator import ContextFileCreator
from modules.main_file_creator_stt import MainFileCreator
from modules.simple_file_creator import SimpleFileCreator
from modules.test_file_creator_stt import TestFileCreator
from modules.helpers.helper import Helper

class StructureHelper:
    def __init__(self, project_structure, root_module):
        self.project_structure = project_structure
        self.root_module = root_module

    def create_directory_structure(self, root_path):
        context_name = self.project_structure["context"]
        context_name_snake = Helper.convert_to_snake_case(self, context_name)

        # Define the root directory for the module
        if self.root_module:
            root_module_path = os.path.join(root_path, *self.root_module.split('.'))
        else:
            root_module_path = root_path

        # Define directories based on the context name
        context_root_dir = os.path.join(root_module_path, context_name_snake)
        states_dir = os.path.join(context_root_dir, "states")
        abstract_state_dir = os.path.join(states_dir, "abstract")
        tests_dir = os.path.join(context_root_dir, "tests")

        # Create directories dynamically
        os.makedirs(abstract_state_dir, exist_ok=True)
        os.makedirs(states_dir, exist_ok=True)
        os.makedirs(tests_dir, exist_ok=True)

        return context_root_dir, states_dir, abstract_state_dir, tests_dir, root_module_path

class StateProjectCreator:
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
        context_root_dir, states_dir, abstract_state_dir, tests_dir, root_module_path = self.helper.create_directory_structure(self.project_name)

        # Create __init__.py files in necessary directories
        SimpleFileCreator(os.path.join(context_root_dir, "__init__.py")).create_simple_file("")
        SimpleFileCreator(os.path.join(states_dir, "__init__.py")).create_simple_file("")
        SimpleFileCreator(os.path.join(abstract_state_dir, "__init__.py")).create_simple_file("")
        SimpleFileCreator(os.path.join(tests_dir, "__init__.py")).create_simple_file("")

        # Create the pytest.ini file
        pytest_ini_path = os.path.join(self.project_name, "pytest.ini")
        SimpleFileCreator(pytest_ini_path).create_simple_file("[pytest]\npythonpath = .\n")

        # Create the abstract state file
        abstract_state_filename = os.path.join(abstract_state_dir, "state.py")
        abstract_state_creator = AbstractStateFileCreator(abstract_state_filename, self.root_module)
        abstract_state_creator.create_abstract_state_file(self.project_structure)

        # Create concrete state files
        for state_name in self.project_structure["state_transitions"].keys():
            state_filename = os.path.join(states_dir, Helper.convert_to_snake_case(self, f"{state_name}_state") + ".py")
            concrete_state_creator = ConcreteStateFileCreator(state_filename, self.root_module)
            concrete_state_creator.create_concrete_state_file(state_name, self.project_structure)

        # Create the context file
        context_filename = os.path.join(context_root_dir, Helper.convert_to_snake_case(self, self.project_structure["context"]) + ".py")
        context_creator = ContextFileCreator(context_filename, self.root_module)
        context_creator.create_context_file(self.project_structure)

        # Create test files
        for state_name in self.project_structure["state_transitions"].keys():
            test_filename = os.path.join(tests_dir, f"test_{Helper.convert_to_snake_case(self, state_name)}_state.py")
            test_creator = TestFileCreator(test_filename, self.root_module)
            test_creator.create_test_file(state_name, self.project_structure)

        # Create the main file
        main_filename = os.path.join(self.project_name, "main.py")
        main_creator = MainFileCreator(main_filename, self.root_module)
        main_creator.create_main_file(self.project_structure)

if __name__ == "__main__":
    project_structure = {
        "context": "Elevator",
        "default_state": "Idle",
        "state_transitions": {
            "Idle": ["MovingUp", "MovingDown"],
            "MovingUp": ["Idle", "MovingDown"],
            "MovingDown": ["Idle", "MovingUp"]
        },
        "properties": [
            "current_floor",
            "max_capacity"
        ],
        "methods": [
            "move_to_floor",
            "emergency_stop"
        ]
    }

    root_module = ""  # Example root module
    creator = StateProjectCreator("ElevatorProject", project_structure, root_module)
    creator.create_project()
