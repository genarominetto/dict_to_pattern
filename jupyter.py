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

