from modules.helpers.helper import Helper

class MainFileCreator:
    def __init__(self, filename, root_module=None):
        self.filename = filename
        self.helper = Helper(filename, root_module)

    def create_main_file(self, project_structure):
        # Extract names from project_structure
        component_name = project_structure.get('component', 'Component')
        composite_name = project_structure.get('composite', 'Composite')
        leaves = project_structure.get('leaves', [])
        leaf_properties = project_structure.get('leaf_properties', {})

        # Convert names to snake_case
        component_snake = Helper.convert_to_snake_case(component_name)
        composite_snake = Helper.convert_to_snake_case(composite_name)

        # Import statements
        # Import the composite class
        composite_import_path = f"{component_snake}.components.composite.{composite_snake}"
        self.helper.write_import_line(composite_import_path, composite_name)

        # Import the leaf classes
        for leaf in leaves:
            leaf_snake = Helper.convert_to_snake_case(leaf)
            leaf_import_path = f"{component_snake}.components.leaves.{leaf_snake}"
            self.helper.write_import_line(leaf_import_path, leaf)

        self.helper.write_empty_line()

        # Start main block
        self.helper.write_code_line(0, 'if __name__ == "__main__":')
        self.helper.write_empty_line()

        # Create instances of leaves
        for leaf in leaves:
            leaf_instance_name1 = f"{leaf.lower()}1"
            leaf_instance_name2 = f"{leaf.lower()}2"
            # Generate initialization parameters
            init_params = ', '.join([f'{key}={repr(value)}' for key, value in leaf_properties.items()])
            # Write code to create two instances of each leaf
            self.helper.write_code_line(1, f'{leaf_instance_name1} = {leaf}(name="{leaf}1", {init_params})')
            self.helper.write_code_line(1, f'{leaf_instance_name2} = {leaf}(name="{leaf}2", {init_params})')
            self.helper.write_empty_line()

        # Create instances of composites
        composite_instance_name1 = f"{composite_name.lower()}1"
        composite_instance_name2 = f"{composite_name.lower()}2"

        self.helper.write_code_line(1, f'{composite_instance_name1} = {composite_name}(name="{composite_name}1")')
        self.helper.write_code_line(1, f'{composite_instance_name2} = {composite_name}(name="{composite_name}2")')
        self.helper.write_empty_line()

        # Add leaves to composites
        leaf_names = [leaf.lower() for leaf in leaves]
        if len(leaf_names) >= 2:
            leaf1_instance_name1 = f"{leaf_names[0]}1"
            leaf2_instance_name1 = f"{leaf_names[1]}1"
            leaf1_instance_name2 = f"{leaf_names[0]}2"
            leaf2_instance_name2 = f"{leaf_names[1]}2"

            self.helper.write_code_line(1, f'{composite_instance_name1}.add({leaf1_instance_name1})')
            self.helper.write_code_line(1, f'{composite_instance_name1}.add({leaf2_instance_name1})')
            self.helper.write_code_line(1, f'{composite_instance_name2}.add({leaf1_instance_name2})')
            self.helper.write_code_line(1, f'{composite_instance_name2}.add({leaf2_instance_name2})')
            self.helper.write_empty_line()

            # Remove one leaf from composite1
            self.helper.write_code_line(1, f'{composite_instance_name1}.remove({leaf2_instance_name1})')
            self.helper.write_empty_line()

            # Add composite2 to composite1
            self.helper.write_code_line(1, f'{composite_instance_name1}.add({composite_instance_name2})')
            self.helper.write_empty_line()
        else:
            # If less than two leaves, adjust accordingly
            for leaf_instance_name in [f"{leaf.lower()}1" for leaf in leaves]:
                self.helper.write_code_line(1, f'{composite_instance_name1}.add({leaf_instance_name})')
            self.helper.write_empty_line()

        # Define a function for operation_func
        self.helper.write_code_line(1, f'def get_{component_name.lower()}_name({component_name.lower()}):')
        self.helper.write_code_line(2, f'return {component_name.lower()}.name')
        self.helper.write_empty_line()

        # Execute operation recursively
        # Assuming we want to collect names of the first leaf type
        if leaves:
            leaf_class_name = leaves[0]
            self.helper.write_code_line(1, f'{leaf_class_name.lower()}_names = {composite_instance_name1}.execute_operation_recursively(')
            self.helper.write_code_line(2, f'operation_func=get_{component_name.lower()}_name,')
            self.helper.write_code_line(2, f'condition_func=isinstance,')
            self.helper.write_code_line(2, f'condition_args=({leaf_class_name},),')
            self.helper.write_code_line(1, f')')
        else:
            # If no leaves are specified
            self.helper.write_code_line(1, f'{component_name.lower()}_names = []')
        self.helper.write_empty_line()

        # Calculate depth
        self.helper.write_code_line(1, f'depth = {composite_instance_name1}.calculate_depth()')
        self.helper.write_empty_line()

        # Print statements
        self.helper.write_code_line(1, f'print({composite_instance_name1})')
        self.helper.write_code_line(1, f'print(f"Is {composite_instance_name1} composite? {{{composite_instance_name1}.is_composite()}}")')

        # Iterate over boolean leaf properties starting with 'is_'
        for prop_name, prop_value in leaf_properties.items():
            if isinstance(prop_value, bool) and prop_name.startswith('is_'):
                method_name = f'any_{prop_name[3:]}'  # Remove 'is_' prefix
                self.helper.write_code_line(1, f'print(f"Does {composite_instance_name1} have any {prop_name[3:]} elements? {{{composite_instance_name1}.{method_name}()}}")')

        self.helper.write_code_line(1, f'print(f"{composite_name}1 ID: {{{composite_instance_name1}.id}}")')
        self.helper.write_code_line(1, f'print(f"Number of children in {composite_instance_name1}: {{len({composite_instance_name1}.get_children())}}")')
        if leaves:
            self.helper.write_code_line(1, f'print(f"{leaf_class_name} names in {composite_instance_name1}: {{{leaf_class_name.lower()}_names}}")')
        else:
            self.helper.write_code_line(1, f'print(f"No leaves specified.")')
        self.helper.write_code_line(1, f'print(f"Depth of {composite_instance_name1} hierarchy: {{depth}}")')
        self.helper.write_empty_line()

        # Save the file
        self.helper.save()
