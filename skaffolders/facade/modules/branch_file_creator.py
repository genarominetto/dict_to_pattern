
# modules/branch_file_creator.py

from modules.helpers.helper import Helper

class BranchFileCreator:
    def __init__(self, filename):
        self.filename = filename
        self.helper = Helper(filename)

    def _ladder_to_import_line(self, ladder):
        module_path = '.'.join([element.lower() + '_modules' for element in ladder[:-1]])
        last_module = ladder[-1].lower()
        class_name = ladder[-1]
        return f"{ladder[0].lower()}.{module_path}.{last_module} import {class_name}"

    def create_branch_file(self, class_name, subcomponents_ladders):
        # Write imports for subcomponents
        for ladder in subcomponents_ladders:
            import_line = self._ladder_to_import_line(ladder)
            self.helper.write_import_line(*import_line.split(' import '))

        # Write the class definition
        self.helper.write_empty_line()
        self.helper.write_code_line(0, f'class {class_name}:')
        self.helper.write_code_line(1, 'def __init__(self):')

        # Write the initialization of subcomponents
        for ladder in subcomponents_ladders:
            component_name = ladder[-1]
            self.helper.write_code_line(2, f'self.{component_name.lower()} = {component_name}()')

        self.helper.save()
