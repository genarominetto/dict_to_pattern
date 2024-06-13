# modules/branch_file_creator.py

from modules.helpers.helper import Helper

class BranchFileCreator:
    def __init__(self, filename):
        self.filename = filename
        self.helper = Helper(filename)

    def create_branch_file(self, class_name, subcomponents_ladders):
        print(f"Subcomponents ladders: {subcomponents_ladders}")
        # Write imports for subcomponents
        for ladder in subcomponents_ladders:
            module_path = '.'.join([segment.lower() for segment in ladder[:-1]])
            component = ladder[-1]
            self.helper.write_import_line(module_path, component)

        # Write the class definition
        self.helper.write_empty_line()
        self.helper.write_code_line(0, f'class {class_name}:')
        self.helper.write_code_line(1, 'def __init__(self):')

        # Write the initialization of subcomponents
        for ladder in subcomponents_ladders:
            component_name = ladder[-1].lower()
            self.helper.write_code_line(2, f'self.{component_name} = {component_name.capitalize()}()')

        self.helper.save()
