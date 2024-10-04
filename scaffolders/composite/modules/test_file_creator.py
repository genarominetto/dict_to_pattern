from modules.helpers.helper import Helper
from jinja2 import Template
import os

class TestFileCreator:
    def __init__(self, filename, root_module=None):
        self.filename = filename
        self.helper = Helper(filename, root_module)

    def create_test_file(self, project_structure, leaf_name):
        # Load the template
        template_path = os.path.join(
            os.path.dirname(__file__),
            'templates',
            'test.py.jinja2'
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
        root_module = self.helper.root_module

        # Prepare properties for the leaf
        property_names = list(leaf_properties.keys())
        property_types = [self.helper.infer_type(type(value)) for value in leaf_properties.values()]
        property_defaults = list(leaf_properties.values())

        # Prepare properties as list of dictionaries
        properties = []
        for name, type_hint, default in zip(property_names, property_types, property_defaults):
            properties.append({
                'name': name,
                'type': type_hint,
                'default': default,
            })

        # Prepare leaf arguments for test cases
        leaf_args = ', '.join([f"{prop['name']}={repr(prop['default'])}" for prop in properties])

        context = {
            'component_name': component_name,
            'component_name_lower': component_name.lower(),
            'composite_name': composite_name,
            'composite_name_lower': composite_name.lower(),
            'leaves': leaves,
            'first_leaf': leaf_name,
            'first_leaf_lower': leaf_name.lower(),
            'properties': properties,
            'leaf_args': leaf_args,
            'root_module': root_module,
            'repr': repr
        }

        # Render the template
        output = template.render(context)

        # Write the output to the file
        with open(self.filename, 'w') as f:
            f.write(output)
