# modules/branch_file_creator.py

from modules.helpers.helper import Helper

class BranchFileCreator:
    def __init__(self, filename):
        self.filename = filename
        self.helper = Helper(filename)

    def create_branch_file(self, class_name, subcomponents):
        # Write imports for subcomponents
        for component in subcomponents:
            module_path = component.replace('.', '/')
            self.helper.write_import_line(module_path, component.split('.')[-1].capitalize())

        # Write the class definition
        self.helper.write_empty_line()
        self.helper.write_code_line(0, f'class {class_name}:')
        self.helper.write_code_line(1, 'def __init__(self):')

        # Write the initialization of subcomponents
        for component in subcomponents:
            component_name = component.split('.')[-1].lower()
            self.helper.write_code_line(2, f'self.{component_name} = {component.split(".")[-1].capitalize()}()')

        self.helper.save()
