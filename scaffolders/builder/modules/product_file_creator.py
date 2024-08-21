from modules.helpers.helper import Helper

class ProductFileCreator:
    def __init__(self, filename, root_module=None):
        self.filename = filename
        self.helper = Helper(filename, root_module)

    def create_product_file(self, project_structure):
        # Extract the product name and convert it to snake_case
        product_name = project_structure["product"]
        product_name_snake = self._convert_to_snake_case(product_name)

        # Write the class definition
        self.helper.write_code_line(0, f'class {product_name}:')
        self.helper.write_code_line(1, f'def __init__(self, {product_name_snake}_type):')
        self.helper.write_code_line(2, f'self.{product_name_snake}_type = {product_name_snake}_type')

        # Initialize all parts as None
        for part in project_structure["parts"]:
            part_name_snake = self._convert_to_snake_case(part)
            self.helper.write_code_line(2, f'self.{part_name_snake} = None')

        # Write setter methods for each part
        for part in project_structure["parts"]:
            part_name_snake = self._convert_to_snake_case(part)
            self.helper.write_empty_line()
            self.helper.write_code_line(1, f'def set_{part_name_snake}(self, {part_name_snake}):')
            self.helper.write_code_line(2, f'self.{part_name_snake} = {part_name_snake}')

        # Write the __str__ method
        self.helper.write_empty_line()
        self.helper.write_code_line(1, f'def __str__(self):')
        self.helper.write_code_line(2, f'return (f"{product_name} of type {{self.{product_name_snake}_type}} with "')
        
        # Write the string representation for each part
        part_strings = []
        for part in project_structure["parts"]:
            part_name_snake = self._convert_to_snake_case(part)
            part_strings.append(f'f"{part_name_snake} {{self.{part_name_snake}}}"')

        self.helper.write_code_line(3, f'{" + ".join(part_strings)} + ".")')

        # Save the file
        self.helper.save()

    def _convert_to_snake_case(self, name):
        # Convert CamelCase to snake_case
        return ''.join(['_' + c.lower() if c.isupper() else c for c in name]).lstrip('_')
