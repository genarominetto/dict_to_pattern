
# modules/helpers/helper.py

class Helper:
    def __init__(self, filepath, root_module=None):
        self.filepath = filepath
        self.root_module = root_module
        self.lines = []

    def write_code_line(self, indentation_level, code_line, newline=True):
        line = ' ' * (indentation_level * 4) + code_line
        if newline:
            line += '\n'
        self.lines.append(line)

    def write_import_line(self, module, class_name, indent_level=0):
        if self.root_module:
            module = f"{self.root_module}.{module}"
        indent = ' ' * (indent_level * 4)
        self.lines.append(f'{indent}from {module} import {class_name}\n')

    def write_empty_line(self):
        self.lines.append('\n')

    @staticmethod
    def convert_to_snake_case(name):
        # Convert CamelCase to snake_case
        return ''.join(['_' + c.lower() if c.isupper() else c for c in name]).lstrip('_')

    def save(self):
        with open(self.filepath, 'w') as file:
            file.writelines(self.lines)

    def infer_type(self, value_type):
        # Map Python types to type hint strings
        if value_type == bool:
            return 'bool'
        elif value_type == int:
            return 'int'
        elif value_type == float:
            return 'float'
        elif value_type == str:
            return 'str'
        elif value_type == list:
            return 'List[Any]'
        elif value_type == dict:
            return 'Dict[str, Any]'
        else:
            return 'Any'






