from modules.helpers.helper import Helper

class DirectorFileCreator:
    def __init__(self, filename, root_module=None):
        self.filename = filename
        self.helper = Helper(filename, root_module)

    def create_director_file(self, project_structure):
        # Extract the product name and convert it to snake_case
        product_name = project_structure["product"]
        product_name_snake = self._convert_to_snake_case(product_name)
        class_name = "Director"

        # Write the import statement for the abstract builder
        self.helper.write_import_line(f'{product_name_snake}_builder.builders.abstract.{product_name_snake}_builder', f'{product_name}Builder')

        # Write the class definition
        self.helper.write_empty_line()
        self.helper.write_code_line(0, f'class {class_name}:')
        self.helper.write_code_line(1, f'def __init__(self, builder: {product_name}Builder):')
        self.helper.write_code_line(2, 'self.builder = builder')

        # Write the method to construct the product
        self.helper.write_empty_line()
        self.helper.write_code_line(1, f'def construct_{product_name_snake}(self):')
        for step in project_structure["parent_steps"]:
            self.helper.write_code_line(2, f'self.builder.{step}()')
        for step in project_structure["child_steps"]:
            self.helper.write_code_line(2, f'self.builder.{step}()')
        self.helper.write_code_line(2, f'return self.builder.get_{product_name_snake}()')

        # Save the file
        self.helper.save()

    def _convert_to_snake_case(self, name):
        # Convert CamelCase to snake_case
        return ''.join(['_' + c.lower() if c.isupper() else c for c in name]).lstrip('_')
