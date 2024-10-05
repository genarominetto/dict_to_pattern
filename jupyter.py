import shutil
import os
from google.colab import files
import subprocess
import sys
import importlib


def format_code_with_black(directory):
    """
    Formats all Python (.py) files in the given directory and its subdirectories using Black.
    
    Parameters:
    directory (str): The path to the directory to format the code.
    """
    
    # Walk through the directory to find .py files
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                
                # Run black formatter on the file
                subprocess.run(["black", file_path])

    print("Code formatting complete.")


def compress_and_download(dir_path):
    # Get the directory name
    dir_name = os.path.basename(os.path.normpath(dir_path))

    # Define the name of the zip file
    zip_file = f"{dir_name}.zip"

    # Temporary directory to hold the project folder
    temp_dir = "/content/temp"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    # Create a new directory inside the temp directory
    temp_project_dir = os.path.join(temp_dir, dir_name)
    shutil.copytree(dir_path, temp_project_dir)

    # Compress the temporary project directory
    shutil.make_archive(os.path.join(temp_dir, dir_name), 'zip', temp_dir, dir_name)

    # Move the zip file to the current directory
    shutil.move(os.path.join(temp_dir, f"{dir_name}.zip"), f"/content/{zip_file}")

    # Clean up the temporary directory
    shutil.rmtree(temp_dir)

    # Download the zip file
    files.download(f"/content/{zip_file}")


def run_tests(test_file_path):
    """
    Run pytest on the specified test file path.

    Parameters:
    test_file_path (str): The path to the test file or directory.

    Returns:
    bool: True if all tests pass, False otherwise.
    """
    result = subprocess.run(['pytest', test_file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(result.stdout.decode())
    print(result.stderr.decode())
    return result.returncode == 0


def print_directory_tree(directory: str):
    """
    Prints a directory tree starting at the specified directory, listing directories first,
    and ignoring files and directories that start with an underscore ('_') or any hidden files.
    """
    file_count = 0
    dir_count = 0
    
    def _tree(dir_path, indent=''):
        nonlocal file_count, dir_count
        # Get list of directories and files
        items = sorted(os.listdir(dir_path))
        dirs = [d for d in items if os.path.isdir(os.path.join(dir_path, d)) and not d.startswith('_') and not d.startswith('.')]
        files = [f for f in items if os.path.isfile(os.path.join(dir_path, f)) and not f.startswith('_') and not f.startswith('.')]
        
        # Increment directory count
        dir_count += len(dirs)
        file_count += len(files)
        
        # Print directories
        for i, d in enumerate(dirs):
            print(f'{indent}├── {d}')
            _tree(os.path.join(dir_path, d), indent + '│   ')
        
        # Print files
        for i, f in enumerate(files):
            if i == len(files) - 1:
                print(f'{indent}└── {f}')
            else:
                print(f'{indent}├── {f}')
    
    print('.')
    _tree(directory)
    print(f'\n{dir_count} directories, {file_count} files')


class ModuleManager:
    def __init__(self, module_paths: dict):
        """
        Initialize the ModuleManager with a dictionary of module names and their paths.
        """
        self.module_paths = module_paths  # e.g., {'facade': '/path/to/facade', ...}
        self.current_module_name = None
        self.current_module_path = None
        self.project_creator_class = None
        self.sys_modules_keys_snapshot = set(sys.modules.keys())

    def set_module(self, module_name: str):
        """
        Set the active module by name. This will handle adding/removing paths and modules.
        """
        if module_name not in self.module_paths:
            raise ValueError(f"Module '{module_name}' not found in module_paths.")

        # Remove current module path and modules if a module is already set
        if self.current_module_name is not None:
            self._remove_current_module()

        # Add new module path
        module_path = self.module_paths[module_name]
        sys.path.insert(0, module_path)
        self.current_module_path = module_path
        self.current_module_name = module_name

        # Take a snapshot of sys.modules keys before importing
        self.sys_modules_keys_snapshot = set(sys.modules.keys())

        # Import the module(s)
        self._import_module(module_name)

    def _import_module(self, module_name: str):
        """
        Import the necessary modules for the specified module name.
        """
        # Build the module import path
        module_import_path = f'dict_to_pattern.scaffolders.{module_name}.{module_name}_project_creator'
        module = importlib.import_module(module_import_path)
        class_name = ''.join([word.capitalize() for word in module_name.split('_')]) + 'ProjectCreator'
        project_creator_class = getattr(module, class_name)
        # Store the class for external access
        self.project_creator_class = project_creator_class

    def _remove_current_module(self):
        """
        Remove the modules imported after the snapshot and the module's path.
        """
        # Remove the module's path from sys.path
        if self.current_module_path in sys.path:
            sys.path.remove(self.current_module_path)

        # Find all modules added since the snapshot
        current_sys_modules_keys = set(sys.modules.keys())
        new_modules = current_sys_modules_keys - self.sys_modules_keys_snapshot

        # Remove the new modules from sys.modules
        for module_name in new_modules:
            del sys.modules[module_name]

        # Reset current module variables
        self.current_module_name = None
        self.current_module_path = None
        self.project_creator_class = None
