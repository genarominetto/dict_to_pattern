# modules/helpers/helper.py

class Helper:
    def __init__(self):
        pass

    def write_code_line(self, indentation_level, code_line):
        return ' ' * (indentation_level * 4) + code_line + '\n'

    def write_import_line(self, module, class_name):
        return f'from {module} import {class_name}\n'
