from modules.helpers.helper import Helper

class ConcreteLeafFileCreator:
    def __init__(self, filename, leaf_name, root_module=None):
        self.filename = filename
        self.leaf_name = leaf_name  # Specify which leaf is being created
        self.helper = Helper(filename, root_module)

    def create_concrete_leaf_file(self, project_structure):
        # Extract necessary information from project_structure
        component_name = project_structure.get('component', 'Component')
        component_snake = Helper.convert_to_snake_case(component_name)
        leaves_dir = 'leaves'
        abstract_leaf_dir = 'abstract'
        abstract_leaf_name = 'leaf'
        abstract_leaf_class_name = abstract_leaf_name.capitalize()

        # Import statement for the abstract leaf class
        import_statement = f'from {component_snake}.components.{leaves_dir}.{abstract_leaf_dir}.{abstract_leaf_name} import {abstract_leaf_class_name}'
        self.helper.write_code_line(0, import_statement)
        self.helper.write_empty_line()

        # Class definition
        leaf_class_name = self.leaf_name
        self.helper.write_code_line(0, f'# Concrete class for {leaf_class_name.lower()}')
        self.helper.write_code_line(0, f'class {leaf_class_name}({abstract_leaf_class_name}):')

        # Prepare the argument list for __init__ method
        leaf_properties = project_structure.get('leaf_properties', {})
        # Start with name
        init_args = ['name: str']
        for key, value in leaf_properties.items():
            type_hint = self.helper.infer_type(type(value))
            init_args.append(f"{key}: {type_hint}")
        # Combine the arguments into a string
        init_args_str = ', '.join(['*'] + init_args)
        self.helper.write_code_line(1, f'def __init__(self, {init_args_str}):')

        # Docstring
        self.helper.write_code_line(2, '"""')
        self.helper.write_code_line(2, f'Initialize a {leaf_class_name.lower()} instance.')
        self.helper.write_code_line(2, '"""')

        # Prepare the list of parameters to pass to super().__init__()
        super_args = [f"{key}={key}" for key in ['name'] + list(leaf_properties.keys())]
        super_args_str = ', '.join(super_args)
        self.helper.write_code_line(2, f'super().__init__({super_args_str})')

        # Save the file
        self.helper.save()
