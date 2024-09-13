from modules.helpers.component_file_builder.builders.abstract.component_file_builder import ComponentFileBuilder
from modules.helpers.helper import Helper

class AbstractLeafComponentFileBuilder(ComponentFileBuilder):
    def __init__(self, filename, project_structure, root_module=None):
        super().__init__(filename, project_structure, root_module)
        self.project_structure = project_structure
        self.helper = Helper(filename, root_module)
        self.leaf_properties = project_structure.get('leaf_properties', {})
        self.root_module = root_module

    def write___init___method(self):
        # Standard library imports
        self.helper.write_code_line(0, 'from typing import Callable, List, Optional, Any, Dict, Union')

        # Project-specific imports using write_import_line
        component_module = self._get_component_module_path()
        component_class_name = self._get_component_class_name()
        self.helper.write_import_line(component_module, component_class_name)
        self.helper.write_empty_line()

        # Class definition
        leaf_class_name = self._get_leaf_class_name()
        self.helper.write_code_line(0, f'class {leaf_class_name}({component_class_name}):')

        # __init__ method signature
        init_params_list = []
        for prop_name, prop_value in self.leaf_properties.items():
            prop_type = self.helper.infer_type(type(prop_value))
            init_params_list.append(f'{prop_name}: {prop_type}')
        init_params = ', '.join(init_params_list)
        self.helper.write_code_line(1, f'def __init__(self, name: str, {init_params}):')

        # Initialize properties
        self.helper.write_code_line(2, 'self.name = name')
        for prop_name in self.leaf_properties.keys():
            self.helper.write_code_line(2, f'self.{prop_name} = {prop_name}')
        self.helper.write_code_line(2, f'super().__init__(name=self.name)')
        self.helper.write_empty_line()

    def write___hash___method(self):
        # Included in target example
        self.helper.write_code_line(1, 'def __hash__(self):')
        self.helper.write_code_line(2, 'return super().__hash__()')
        self.helper.write_empty_line()

    def write___str___method(self):
        # Included in target example
        self.helper.write_code_line(1, 'def __str__(self, level=0) -> str:')
        self.helper.write_code_line(2, 'indent = "    " * level')
        # Build the properties string explicitly
        properties = ', '.join([f'{prop}: {{self.{prop}}}' for prop in self.leaf_properties.keys()])
        self.helper.write_code_line(2, f'return f"{{indent}}{{self.name}} ({properties})"')
        self.helper.write_empty_line()

    def write__ensure_tuple_method(self):
        pass

    def write__generate_id_method(self):
        pass

    def write_any_bool_methods(self):
        # Included in target example
        for prop_name, prop_value in self.leaf_properties.items():
            if isinstance(prop_value, bool):
                if not prop_name.startswith('is_'):
                    raise ValueError(f"Boolean property '{prop_name}' must start with 'is_'")
                method_name = f'any_{prop_name[3:]}'
                self.helper.write_code_line(1, f'def {method_name}(self) -> bool:')
                self.helper.write_code_line(2, f'return self.{prop_name}')
                self.helper.write_empty_line()

    def write__validate_composite_logic_method(self):
        pass

    def write__validate_remove_logic_method(self):
        pass

    def write_validate_structure_method(self):
        pass

    def write_add_method(self):
        # Included in target example
        component_class_name = self._get_component_class_name()
        self.helper.write_code_line(1, f'def add(self, component: {component_class_name}) -> None:')
        self.helper.write_code_line(2, 'raise NotImplementedError("Cannot add components to a leaf.")')
        self.helper.write_empty_line()

    def write_remove_method(self):
        # Included in target example
        component_class_name = self._get_component_class_name()
        self.helper.write_code_line(1, f'def remove(self, component: {component_class_name}) -> None:')
        self.helper.write_code_line(2, 'raise NotImplementedError("Cannot remove components from a leaf.")')
        self.helper.write_empty_line()

    def write_is_composite_method(self):
        # Included in target example
        self.helper.write_code_line(1, 'def is_composite(self) -> bool:')
        self.helper.write_code_line(2, 'return False')
        self.helper.write_empty_line()

    def write_get_children_method(self):
        pass

    def write_remove_components_recursively_method(self):
        # Included in target example
        component_class_name = self._get_component_class_name()
        self.helper.write_code_line(1, 'def remove_components_recursively(')
        self.helper.write_code_line(2, f'self, condition_func: Callable[[{component_class_name}, Any], bool],')
        self.helper.write_code_line(2, 'condition_args: Union[tuple, Any] = ()')
        self.helper.write_code_line(1, f') -> List[{component_class_name}]:')
        self.helper.write_code_line(2, 'return []')
        self.helper.write_empty_line()

    def write_get_components_recursively_method(self):
        # Included in target example
        component_class_name = self._get_component_class_name()
        self.helper.write_code_line(1, 'def get_components_recursively(')
        self.helper.write_code_line(2, f'self, condition_func: Optional[Callable[[{component_class_name}, Any], bool]] = None,')
        self.helper.write_code_line(2, 'condition_args: Union[tuple, Any] = ()')
        self.helper.write_code_line(1, f') -> List[{component_class_name}]:')
        self.helper.write_code_line(2, '# Check if the condition function is provided, if not, return the leaf itself')
        self.helper.write_code_line(2, 'if condition_func:')
        self.helper.write_code_line(3, '# If condition_func evaluates to True, return the leaf')
        self.helper.write_code_line(3, 'if condition_func(self, *condition_args):')
        self.helper.write_code_line(4, 'return [self]')
        self.helper.write_code_line(3, 'else:')
        self.helper.write_code_line(4, 'return []  # Return empty if it doesn\'t meet the condition')
        self.helper.write_code_line(2, 'return [self]  # If no condition, just return the leaf itself')
        self.helper.write_empty_line()

    def write_execute_operation_recursively_method(self):
        # Included in target example
        component_class_name = self._get_component_class_name()
        self.helper.write_code_line(1, 'def execute_operation_recursively(')
        self.helper.write_code_line(2, f'self, operation_func: Callable[[{component_class_name}, Any], Any],')
        self.helper.write_code_line(2, 'operation_args: Union[tuple, Any] = (),')
        self.helper.write_code_line(2, f'condition_func: Optional[Callable[[{component_class_name}, Any], bool]] = None,')
        self.helper.write_code_line(2, 'condition_args: Union[tuple, Any] = (),')
        self.helper.write_code_line(1, ') -> List[Any]:')
        self.helper.write_code_line(2, 'operation_args = self._ensure_tuple(operation_args)')
        self.helper.write_code_line(2, 'condition_args = self._ensure_tuple(condition_args)')
        self.helper.write_code_line(2, 'results = []')
        self.helper.write_code_line(2, 'if condition_func is None or condition_func(self, *condition_args):')
        self.helper.write_code_line(3, 'result = operation_func(self, *operation_args)')
        self.helper.write_code_line(3, 'results.append(result)')
        self.helper.write_code_line(2, 'return results')
        self.helper.write_empty_line()

    def write_get_structure_as_dict_method(self):
        # Included in target example
        self.helper.write_code_line(1, 'def get_structure_as_dict(self) -> Dict:')
        self.helper.write_code_line(2, 'return {self.name: {}}')
        self.helper.write_empty_line()

    def write_is_leaf_method(self):
        # Included in target example
        self.helper.write_code_line(1, 'def is_leaf(self) -> bool:')
        self.helper.write_code_line(2, 'return True')
        self.helper.write_empty_line()

    def write_id_method(self):
        pass

    def write_calculate_depth_method(self):
        # Included in target example
        self.helper.write_code_line(1, 'def calculate_depth(self) -> int:')
        self.helper.write_code_line(2, 'return 1  # A leaf has a depth of 1')
        self.helper.write_empty_line()

    def write_get_parents_method(self):
        pass

    def write_clone_method(self):
        pass

    def write__undo_add_method(self):
        pass

    def write__undo_remove_method(self):
        pass

    def write_export_to_pickle_method(self):
        pass

    def write_import_from_pickle_method(self):
        pass

    def save_file(self):
        self.helper.save()

    # Helper methods to avoid using specific values from project_structure
    def _get_component_class_name(self):
        # Use the key 'component' capitalized
        return self.project_structure.get('component', 'Component').capitalize()

    def _get_leaf_class_name(self):
        # Return a generic name for the leaf class
        return 'Leaf'

    def _get_component_module_path(self):
        # Use the key 'component' in snake_case for module paths
        component_name_snake = Helper.convert_to_snake_case(self.project_structure.get('component', 'component'))
        return f"{component_name_snake}.abstract.{component_name_snake}"

    def _ensure_tuple(self, args):
        if isinstance(args, tuple):
            return args
        return (args,)
