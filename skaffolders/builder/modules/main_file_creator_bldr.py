from modules.helpers.helper import Helper

class MainFileCreator:
    def __init__(self, filename, root_module=None):
        self.filename = filename
        self.helper = Helper(filename, root_module)

    def create_main_file(self, project_structure):
        product_name = project_structure["product"]
        product_name_snake = self._convert_to_snake_case(product_name)
        builders = project_structure["types"]

        # Write import statements for each builder and the director
        for builder in builders:
            builder_name_snake = self._convert_to_snake_case(builder)
            self.helper.write_import_line(f'{product_name_snake}_builder.builders.{builder_name_snake}_{product_name_snake}_builder', f'{builder}{product_name}Builder')
        self.helper.write_import_line(f'{product_name_snake}_builder.director', 'Director')

        # Write the main function
        self.helper.write_empty_line()
        self.helper.write_code_line(0, 'def main():')

        # Instantiate each builder and use the director to construct the product
        for builder in builders:
            builder_name_snake = self._convert_to_snake_case(builder)
            self.helper.write_code_line(1, f'{builder_name_snake}_builder = {builder}{product_name}Builder()')
            self.helper.write_code_line(1, f'director = Director({builder_name_snake}_builder)')
            self.helper.write_code_line(1, f'{builder_name_snake}_{product_name_snake} = director.construct_{product_name_snake}()')
            self.helper.write_code_line(1, f'print({builder_name_snake}_{product_name_snake})')
            self.helper.write_empty_line()

        # Write the entry point check
        self.helper.write_code_line(0, 'if __name__ == "__main__":')
        self.helper.write_code_line(1, 'main()')

        # Save the file
        self.helper.save()

    def _convert_to_snake_case(self, name):
        # Convert CamelCase to snake_case
        return ''.join(['_' + c.lower() if c.isupper() else c for c in name]).lstrip('_')
