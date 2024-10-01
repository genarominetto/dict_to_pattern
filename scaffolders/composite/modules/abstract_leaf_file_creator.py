from modules.helpers.helper import Helper
from jinja2 import Template
import os

class AbstractLeafFileCreator:
    def __init__(self, filename, root_module=None):
        self.filename = filename
        self.helper = Helper(filename, root_module)

    def create_abstract_leaf_file(self, project_structure):
        # Load the template
        template_path = os.path.join(
            os.path.dirname(__file__),
            'templates',
            'abstract_leaf.py.jinja2'
        )
        with open(template_path, 'r') as template_file:
            template_content = template_file.read()

        # Create a Jinja2 Template from the file content
        template = Template(template_content)

        # Prepare context for the template
        component_name = project_structure['component']
        component_name_snake = Helper.convert_to_snake_case(component_name)
        leaf_properties = project_structure.get('leaf_properties', {})

        # Collect property names, types, and values
        property_names = list(leaf_properties.keys())
        property_types = [self.helper.infer_type(type(value)) for value in leaf_properties.values()]
        property_values = list(leaf_properties.values())

        # Prepare properties as a list of dictionaries
        properties = []
        for name, type_hint, value in zip(property_names, property_types, property_values):
            properties.append({
                'name': name,
                'type': type_hint,
                'value': value,
            })

        # Extract boolean properties starting with 'is_' for any_* methods
        bool_methods = []
        for prop in properties:
            if prop['type'] == 'bool' and prop['name'].startswith('is_'):
                method_name = 'any_' + prop['name'][3:]
                bool_methods.append({
                    'method_name': method_name,
                    'property_name': prop['name']
                })

        context = {
            'component_name': component_name,
            'component_name_snake': component_name_snake,
            'properties': properties,
            'bool_methods': bool_methods,
            'root_module': self.helper.root_module,
        }

        # Render the template
        output = template.render(context)

        # Write the output to the file
        with open(self.filename, 'w') as f:
            f.write(output)
