# .github/scripts/scaffold_and_test.py

import os
import subprocess
import sys
from dict_to_pattern.skaffolders.facade.project_creator import FacadeProjectCreator

def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    if process.returncode != 0:
        print(f"Error running command: {command}")
        print(err.decode("utf-8"))
        sys.exit(1)
    return out.decode("utf-8")

def scaffold_and_test():
    project_name = 'FacadeProject'
    project_structure = {
        'Car': {
            'Engine': {
                'Cylinders': {},
                'Pistons': {}
            },
            'Chassis': {}
        },
        'Driver': {}
    }

    # Create the project using the FacadeProjectCreator
    creator = FacadeProjectCreator(project_name, project_structure)
    creator.create_project()

    # Run tests
    os.chdir(project_name)
    test_result = run_command("pytest --junitxml=results.xml")
    print(test_result)

if __name__ == "__main__":
    scaffold_and_test()

