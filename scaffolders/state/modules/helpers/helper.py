# modules/helpers/helper.py

class Helper:
    def __init__(self, filepath, root_module=None):
        self.filepath = filepath
        self.root_module = root_module
        self.lines = []

    def write_code_line(self, indentation_level, code_line):
        self.lines.append(' ' * (indentation_level * 4) + code_line + '\n')

    def write_import_line(self, module, class_name):
        """
        Add an import line in the format 'from module import class_name' to the file.
        This method does not support 'import module' format.
        Use the write_code_line method for other types of import statements.
        """
        if self.root_module:
            module = f"{self.root_module}.{module}"
        self.lines.append(f'from {module} import {class_name}\n')

    def write_empty_line(self):
        self.lines.append('\n')
        
    def convert_to_snake_case(self, name):
        # Convert CamelCase to snake_case
        return ''.join(['_' + c.lower() if c.isupper() else c for c in name]).lstrip('_')

    def save(self):
        with open(self.filepath, 'w') as file:
            file.writelines(self.lines)
