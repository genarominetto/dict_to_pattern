
# modules/helpers/helper.py

class Helper:
    def __init__(self, filepath, root_module=None):
        self.filepath = filepath
        self.root_module = root_module
        self.lines = []

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
            return 'list'
        elif value_type == dict:
            return 'dict'
        else:
            return 'any'
        
    @staticmethod
    def convert_to_snake_case(name):
        # Convert CamelCase to snake_case
        return ''.join(['_' + c.lower() if c.isupper() else c for c in name]).lstrip('_')






