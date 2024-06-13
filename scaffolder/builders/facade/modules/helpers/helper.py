# modules/helpers/helper.py

class Helper:
    def __init__(self, filepath):
        self.filepath = filepath
        self.lines = []

    def write_code_line(self, indentation_level, code_line):
        self.lines.append(' ' * (indentation_level * 4) + code_line + '\n')

    def write_import_line(self, module, class_name):
        if class_name:
            self.lines.append(f'from {module} import {class_name}\n')
        else:
            self.lines.append(f'import {module}\n')

    def write_empty_line(self):
        self.lines.append('\n')

    def save(self):
        with open(self.filepath, 'w') as file:
            file.writelines(self.lines)
