from modules.helpers.helper import Helper
from jinja2 import Template
import os

class AbstractComponentFileCreator:
    def __init__(self, filename, root_module=None):
        self.filename = filename
        self.helper = Helper(filename, root_module)

    def create_abstract_component_file(self, project_structure):
        # Load the template
        template_path = os.path.join(
            os.path.dirname(__file__),
            'templates',
            'abstract_component.py.jinja2'
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

        # Extract boolean properties where the key starts with 'is_'
        bool_properties = {}
        for key, value in leaf_properties.items():
            if isinstance(value, bool) and key.startswith('is_'):
                method_name = 'any_' + key[3:]
                bool_properties[method_name] = value

        context = {
            'component_name': component_name,
            'component_name_snake': Helper.convert_to_snake_case(component_name),
            'composite_name': composite_name,
            'composite_name_snake': Helper.convert_to_snake_case(composite_name),
            'leaves': leaves,
            'leaf_properties': leaf_properties,
            'bool_methods': bool_properties,
            'root_module': self.helper.root_module,
        }

        # Render the template
        output = template.render(context)

        # Write the output to the file
        with open(self.filename, 'w') as f:
            f.write(output)
