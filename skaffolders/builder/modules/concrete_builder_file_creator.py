from modules.helpers.helper import Helper

class ConcreteBuilderFileCreator:
    def __init__(self, filename, root_module=None):
        self.filename = filename
        self.helper = Helper(filename, root_module)

    def create_concrete_builder_file(self, product_type, project_structure):
        # Extract the product name and convert it to snake_case
        product_name = project_structure["product"]
        product_name_snake = self._convert_to_snake_case(product_name)

        # Convert the type to snake_case
        type_snake = self._convert_to_snake_case(product_type)

        # Define the concrete builder class name
        class_name = f"{product_type}{product_name}Builder"

        # Write the import statements
        self.helper.write_import_line(f'{product_name_snake}_builder.builders.abstract.{product_name_snake}_builder', f'{product_name}Builder')
        for part in project_structure['parts']:
            part_snake = self._convert_to_snake_case(part)
            self.helper.write_import_line(f'{product_name_snake}_builder.product.{product_name_snake}_parts.{part_snake}', part)

        # Write the class definition
        self.helper.write_empty_line()
        self.helper.write_code_line(0, f'class {class_name}({product_name}Builder):')
        self.helper.write_code_line(1, f'def __init__(self):')
        self.helper.write_code_line(2, f'super().__init__("{product_type}")')

        # Initialize the parts in the constructor
        for part in project_structure['parts']:
            part_snake = self._convert_to_snake_case(part)
            self.helper.write_code_line(2, f'self.{part_snake} = {part}()')

        # Implement the child steps
        for step in project_structure["child_steps"]:
            self.helper.write_empty_line()
            self.helper.write_code_line(1, f'def {step}(self):')
            self.helper.write_code_line(2, f'print("Doing {step} for {product_type}")')

        # Save the file
        self.helper.save()

    def _convert_to_snake_case(self, name):
        # Convert CamelCase to snake_case
        return ''.join(['_' + c.lower() if c.isupper() else c for c in name]).lstrip('_')
