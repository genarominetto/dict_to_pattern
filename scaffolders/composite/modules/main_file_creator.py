from modules.helpers.helper import Helper
from jinja2 import Template
import os

class MainFileCreator:
    def __init__(self, filename, root_module=None):
        self.filename = filename
        self.helper = Helper(filename, root_module)

    def create_main_file(self, project_structure):
        # Load the template
        template_path = os.path.join(
            os.path.dirname(__file__),
            'templates',
            'main.py.jinja2'
        )
        with open(template_path, 'r') as template_file:
            template_content = template_file.read()

        # Create a Jinja2 Template from the file content
        template = Template(template_content)

        # Prepare context for the template
        component_name = project_structure['component']
        composite_name = project_structure['composite']
        leaves = project_structure['leaves']
        leaf_properties = project_structure.get('leaf_properties', {})

        # Convert names to snake_case
        component_name_snake = Helper.convert_to_snake_case(component_name)
        composite_name_snake = Helper.convert_to_snake_case(composite_name)
        leaves_snake = [Helper.convert_to_snake_case(leaf) for leaf in leaves]

        # Collect property names and default values
        property_assignments = []
        for name, value in leaf_properties.items():
            if isinstance(value, str):
                value_repr = f'"{value}"'
            else:
                value_repr = value
            property_assignments.append({
                'name': name,
                'value': value_repr
            })

        context = {
            'component_name': component_name,
            'component_name_snake': component_name_snake,
            'composite_name': composite_name,
            'composite_name_snake': composite_name_snake,
            'leaves': leaves,
            'leaves_snake': leaves_snake,
            'leaf_properties': property_assignments,
            'root_module': self.helper.root_module,
            'zip': zip
        }

        # Render the template
        output = template.render(context)

        # Write the output to the file
        with open(self.filename, 'w') as f:
            f.write(output)
