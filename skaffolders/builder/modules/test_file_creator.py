from modules.helpers.helper import Helper

class TestFileCreator:
    def __init__(self, filename, root_module=None):
        self.filename = filename
        self.helper = Helper(filename, root_module)

    def create_test_file(self, type_name, project_structure):
        # Convert the product name and type name to snake_case
        product_name = project_structure["product"]
        product_name_snake = self._convert_to_snake_case(product_name)
        type_name_snake = self._convert_to_snake_case(type_name)
        
        # Write import statements
        self.helper.write_import_line('pytest', '')
        self.helper.write_import_line(f'{product_name_snake}_builder.builders.{type_name_snake}_{product_name_snake}_builder', f'{type_name}{product_name}Builder')
        self.helper.write_import_line(f'{product_name_snake}_builder.director', 'Director')

        # Write the test function
        self.helper.write_empty_line()
        self.helper.write_code_line(0, f'def test_{type_name_snake}_{product_name_snake}():')
        self.helper.write_code_line(1, f'builder = {type_name}{product_name}Builder()')
        self.helper.write_code_line(1, f'director = Director(builder)')
        self.helper.write_code_line(1, f'{product_name_snake} = director.construct_{product_name_snake}()')

        # Write assertions for each part
        self.helper.write_empty_line()
        self.helper.write_code_line(1, f'assert "{type_name}" in str({product_name_snake})')
        for part in project_structure["parts"]:
            self.helper.write_code_line(1, f'assert "{part}" in str({product_name_snake})')

        # Save the file
        self.helper.save()

    def _convert_to_snake_case(self, name):
        # Convert CamelCase to snake_case
        return ''.join(['_' + c.lower() if c.isupper() else c for c in name]).lstrip('_')
