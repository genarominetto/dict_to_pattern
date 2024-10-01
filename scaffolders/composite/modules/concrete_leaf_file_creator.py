from modules.helpers.helper import Helper
from jinja2 import Template
import os

class ConcreteLeafFileCreator:
    def __init__(self, filename, root_module=None):
        self.filename = filename
        self.helper = Helper(filename, root_module)

    def create_concrete_leaf_files(self, project_structure, leaf_name):
        # Load the template
        template_path = os.path.join(
            os.path.dirname(__file__),
            'templates',
            'concrete_leaf.py.jinja2'
        )
        with open(template_path, 'r') as template_file:
            template_content = template_file.read()

        # Create a Jinja2 Template from the file content
        template = Template(template_content)

        # Prepare context for the template
        component_name = project_structure['component']
        component_name_snake = Helper.convert_to_snake_case(component_name)
        leaf_properties = project_structure.get('leaf_properties', {})
        leaf_class_name = leaf_name
        leaf_class_name_snake = Helper.convert_to_snake_case(leaf_class_name)

        # Collect property names and types
        property_names = list(leaf_properties.keys())
        property_types = [self.helper.infer_type(type(value)) for value in leaf_properties.values()]

        # Prepare properties as a list of dictionaries
        properties = []
        for name, type_hint in zip(property_names, property_types):
            properties.append({
                'name': name,
                'type': type_hint,
            })

        context = {
            'component_name': component_name,
            'component_name_snake': component_name_snake,
            'leaf_class_name': leaf_class_name,
            'leaf_class_name_snake': leaf_class_name_snake,
            'properties': properties,
            'root_module': self.helper.root_module,
        }

        # Render the template
        output = template.render(context)

        # Write the output to the file
        with open(self.filename, 'w') as f:
            f.write(output)
