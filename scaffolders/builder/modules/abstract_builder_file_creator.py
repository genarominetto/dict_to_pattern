from modules.helpers.helper import Helper

class AbstractBuilderFileCreator:
    def __init__(self, filename, root_module=None):
        self.filename = filename
        self.helper = Helper(filename, root_module)

    def create_abstract_builder_file(self, project_structure):
        # Extract the product name
        product_name = project_structure["product"]
        product_name_snake = self._convert_to_snake_case(product_name)
        class_name = f"{product_name}Builder"

        # Write the import statements
        self.helper.write_code_line(0, 'from abc import ABC')
        self.helper.write_code_line(0, 'from abc import abstractmethod')
        self.helper.write_import_line(f'{product_name_snake}_builder.product.{product_name_snake}', product_name)

        # Write the class definition
        self.helper.write_empty_line()
        self.helper.write_code_line(0, f'class {class_name}(ABC):')
        self.helper.write_code_line(1, f'def __init__(self, {product_name_snake}_type):')
        self.helper.write_code_line(2, f'self.{product_name_snake} = {product_name}({product_name_snake}_type)')

        # Write the parent steps as methods
        for step in project_structure["parent_steps"]:
            self.helper.write_empty_line()
            self.helper.write_code_line(1, f'def {step}(self):')
            self.helper.write_code_line(2, f'print("Doing {step}")')

        # Write the child steps as abstract methods
        for step in project_structure["child_steps"]:
            self.helper.write_empty_line()
            self.helper.write_code_line(1, f'@abstractmethod')
            self.helper.write_code_line(1, f'def {step}(self):')
            self.helper.write_code_line(2, 'pass')

        # Write the get_vacation_house method
        self.helper.write_empty_line()
        self.helper.write_code_line(1, f'def get_{product_name_snake}(self):')
        self.helper.write_code_line(2, f'return self.{product_name_snake}')

        # Save the file
        self.helper.save()

    def _convert_to_snake_case(self, name):
        # Convert CamelCase to snake_case
        return ''.join(['_' + c.lower() if c.isupper() else c for c in name]).lstrip('_')
