from modules.helpers.helper import Helper

class ProductPartFileCreator:
    def __init__(self, filename, root_module=None):
        self.filename = filename
        self.helper = Helper(filename, root_module)

    def create_product_part_file(self, part_name):
        # Convert the part name to snake_case and use CamelCase for the class name
        class_name = part_name
        part_name_snake = self._convert_to_snake_case(part_name)

        # Write the class definition
        self.helper.write_code_line(0, f'class {class_name}:')
        self.helper.write_code_line(1, f'def __init__(self):')
        self.helper.write_code_line(2, 'pass')

        # Write the __str__ method
        self.helper.write_empty_line()
        self.helper.write_code_line(1, 'def __str__(self):')
        self.helper.write_code_line(2, f'return "{class_name}"')

        # Save the file
        self.helper.save()

    def _convert_to_snake_case(self, name):
        # Convert CamelCase to snake_case
        return ''.join(['_' + c.lower() if c.isupper() else c for c in name]).lstrip('_')
