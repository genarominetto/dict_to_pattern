from modules.helpers.helper import Helper
from jinja2 import Template
import os

class ValidatorFileCreator:
    def __init__(self, filename, root_module=None):
        self.filename = filename
        self.helper = Helper(filename, root_module)

    def create_validator_file(self, project_structure):
        # Load the template
        template_path = os.path.join(
            os.path.dirname(__file__),
            'templates',
            'validator.py.jinja2'
        )
        with open(template_path, 'r') as template_file:
            template_content = template_file.read()

        # Create a Jinja2 Template from the file content
        template = Template(template_content)

        # Prepare context for the template
        component_name = project_structure['component']
        component_name_snake = Helper.convert_to_snake_case(component_name)
        component_name_lower = component_name.lower()
        composite_name = project_structure['composite']
        composite_name_snake = Helper.convert_to_snake_case(composite_name)
        composite_name_lower = composite_name.lower()
        root_module = self.helper.root_module

        context = {
            'component_name': component_name,
            'component_name_snake': component_name_snake,
            'component_name_lower': component_name_lower,
            'composite_name': composite_name,
            'composite_name_snake': composite_name_snake,
            'composite_name_lower': composite_name_lower,
            'root_module': root_module,
        }

        # Render the template
        output = template.render(context)

        # Write the output to the file
        with open(self.filename, 'w') as f:
            f.write(output)
