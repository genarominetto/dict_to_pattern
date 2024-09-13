from modules.helpers.helper import Helper

class DataLoaderFileCreator:
    def __init__(self, filename, root_module=None):
        self.filename = filename
        self.helper = Helper(filename, root_module)

    def create_data_loader_file(self, project_structure):
        # Extract the component class name and module path using keys
        component_name = project_structure.get('component', 'Component')
        component_class_name = component_name
        component_instance_name = component_name.lower()
        component_module_path = self._get_component_module_path(project_structure)

        # Start writing the file
        self.helper.write_code_line(0, 'import pickle')
        self.helper.write_empty_line()

        # Write the DataLoader class
        self.helper.write_code_line(0, 'class DataLoader:')
        self.helper.write_code_line(1, f'"""Handles importing and exporting {component_class_name}s using pickle."""')
        self.helper.write_empty_line()

        # Write export_to_pickle method
        self.helper.write_code_line(1, f'def export_to_pickle(self, {component_instance_name}: "{component_class_name}", path: str) -> None:')
        self.helper.write_code_line(2, f'"""Exports the {component_instance_name} structure to a pickle file and renumbers ids starting from 1."""')
        self.helper.write_code_line(2, f'# First, create a new numbering starting from 1 for all components')
        self.helper.write_code_line(2, f'self._renumber_ids({component_instance_name})')
        self.helper.write_empty_line()
        self.helper.write_code_line(2, f'# Save the {component_instance_name} object to the specified path using pickle')
        self.helper.write_code_line(2, 'with open(path, \'wb\') as file:')
        self.helper.write_code_line(3, f'pickle.dump({component_instance_name}, file)')
        self.helper.write_empty_line()

        # Write import_from_pickle method
        self.helper.write_code_line(1, f'def import_from_pickle(self, path: str) -> "{component_class_name}":')
        self.helper.write_code_line(2, f'"""Imports the {component_instance_name} structure from a pickle file and regenerates ids."""')
        self.helper.write_code_line(2, 'with open(path, \'rb\') as file:')
        self.helper.write_code_line(3, f'{component_instance_name} = pickle.load(file)')
        self.helper.write_empty_line()
        self.helper.write_code_line(2, f'# After loading, regenerate the ids using _generate_id')
        self.helper.write_code_line(2, f'self._regenerate_ids({component_instance_name})')
        self.helper.write_empty_line()
        self.helper.write_code_line(2, f'return {component_instance_name}')
        self.helper.write_empty_line()

        # Write _renumber_ids method
        self.helper.write_code_line(1, f'def _renumber_ids(self, {component_instance_name}: "{component_class_name}") -> None:')
        self.helper.write_code_line(2, f'"""Renumbers the ids of all components in the structure, starting from 1."""')
        self.helper.write_code_line(2, 'id_counter = 1')
        self.helper.write_empty_line()
        self.helper.write_code_line(2, f'def renumber({component_instance_name}):')
        self.helper.write_code_line(3, 'nonlocal id_counter')
        self.helper.write_code_line(3, f'{component_instance_name}._id = id_counter  # Assign the new id')
        self.helper.write_code_line(3, 'id_counter += 1')
        self.helper.write_code_line(3, f'for child in {component_instance_name}.get_children():')
        self.helper.write_code_line(4, 'renumber(child)')
        self.helper.write_empty_line()
        self.helper.write_code_line(2, f'renumber({component_instance_name})')
        self.helper.write_empty_line()

        # Write _regenerate_ids method
        self.helper.write_code_line(1, f'def _regenerate_ids(self, {component_instance_name}: "{component_class_name}") -> None:')
        self.helper.write_code_line(2, f'"""Regenerates the ids for all components in the structure using the _generate_id method."""')
        # Import the component class inside the method
        self.helper.write_code_line(2, f'from {component_module_path} import {component_class_name}')
        self.helper.write_empty_line()
        self.helper.write_code_line(2, f'def regenerate({component_instance_name}):')
        self.helper.write_code_line(3, f'{component_instance_name}._id = {component_class_name}._generate_id()  # Regenerate the id')
        self.helper.write_code_line(3, f'for child in {component_instance_name}.get_children():')
        self.helper.write_code_line(4, 'regenerate(child)')
        self.helper.write_empty_line()
        self.helper.write_code_line(2, f'regenerate({component_instance_name})')
        self.helper.write_empty_line()

        # Save the file
        self.helper.save()

    def _get_component_module_path(self, project_structure):
        # Use the keys from project_structure to construct the module path
        component_name = project_structure.get('component', 'Component')
        component_snake = Helper.convert_to_snake_case(component_name)
        # Assume that the component class is in component_name_snake.abstract.component_name_snake
        module_path = f'{component_snake}.abstract.{component_snake}'
        return module_path
