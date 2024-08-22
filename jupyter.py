import shutil
import os
from google.colab import files
import subprocess


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


import os

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
