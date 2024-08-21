from modules.helpers.helper import Helper

class ConcreteBuilderFileCreator:
    def __init__(self, filename, root_module=None):
        self.filename = filename
        self.helper = Helper(filename, root_module)

    def create_concrete_builder_file(self, type_name, project_structure):
        # Extract the product name and convert names to snake_case
        product_name = project_structure["product"]
        product_name_snake = self._convert_to_snake_case(product_name)
        type_name_snake = self._convert_to_snake_case(type_name)
        class_name = f"{type_name}{product_name}Builder"

        # Write import statements
        self.helper.write_import_line(f'{product_name_snake}_builder.builders.abstract.{product_name_snake}_builder', f'{product_name}Builder')
        self.helper.write_import_line(f'{product_name_snake}_builder.product.{product_name_snake}', product_name)
        for part in project_structure['parts']:
            part_name_snake = self._convert_to_snake_case(part)
            self.helper.write_import_line(f'{product_name_snake}_builder.product.{product_name_snake}_parts.{part_name_snake}', part)

        # Write the class definition
        self.helper.write_empty_line()
        self.helper.write_code_line(0, f'class {class_name}({product_name}Builder):')
        self.helper.write_code_line(1, f'def __init__(self):')
        self.helper.write_code_line(2, f'super().__init__("{type_name}")')
        
        # Declare the product parts and set them
        for part in project_structure['parts']:
            part_name_snake = self._convert_to_snake_case(part)
            self.helper.write_code_line(2, f'self.{part_name_snake} = {part}()')
            method_name = f'set_{part_name_snake}'
            self.helper.write_code_line(2, f'self.vacation_house.{method_name}(self.{part_name_snake})')

        # Implement the child steps as methods (without hardcoding part-related logic)
        for step in project_structure["child_steps"]:
            self.helper.write_empty_line()
            self.helper.write_code_line(1, f'def {step}(self):')
            self.helper.write_code_line(2, f'print("Doing {step} for {type_name}")')

        # Save the file
        self.helper.save()

    def _convert_to_snake_case(self, name):
        # Convert CamelCase to snake_case
        return ''.join(['_' + c.lower() if c.isupper() else c for c in name]).lstrip('_')
