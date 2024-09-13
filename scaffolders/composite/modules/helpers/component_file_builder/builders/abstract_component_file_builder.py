from modules.helpers.component_file_builder.builders.abstract.component_file_builder import ComponentFileBuilder
from modules.helpers.helper import Helper

class AbstractComponentFileBuilder(ComponentFileBuilder):
    def __init__(self, filename, project_structure, root_module=None):
        super().__init__(filename, project_structure, root_module)
        self.project_structure = project_structure
        self.helper = Helper(filename, root_module)
        self.leaf_properties = project_structure.get('leaf_properties', {})
        self.root_module = root_module

    def write___init___method(self):
        # Import statements
        self.helper.write_code_line(0, 'from abc import ABC, abstractmethod')
        self.helper.write_code_line(0, 'from typing import Callable, List, Optional, Any, Dict, Union, Set')

        # Project-specific imports using write_import_line
        component_module = self._get_component_module_path()
        component_validator_module = f"{component_module}_modules.{self._get_component_name_snake()}_validator"
        data_loader_module = f"{component_module}_modules.data_loader"
        self.helper.write_import_line(data_loader_module, 'DataLoader')
        validator_class_name = f"{self._get_component_class_name()}Validator"
        self.helper.write_import_line(component_validator_module, validator_class_name)
        self.helper.write_empty_line()

        # Class definition
        component_class_name = self._get_component_class_name()
        self.helper.write_code_line(0, f'class {component_class_name}(ABC):')
        self.helper.write_code_line(1, '"""')
        self.helper.write_code_line(1, 'Abstract base class for all components (both composite and leaf).')
        self.helper.write_code_line(1, '"""')
        self.helper.write_empty_line()

        # Class variables
        self.helper.write_code_line(1, '_id_counter = 0  # Class variable to keep track of the ids across all instances')
        self.helper.write_code_line(1, '_loader = DataLoader()')
        self.helper.write_empty_line()

        # __init__ method
        self.helper.write_code_line(1, 'def __init__(self, name: str):')
        component_class_name = self._get_component_class_name()
        self.helper.write_code_line(2, f"self._parents: List['{component_class_name}'] = []  # Now allowing multiple parents")
        self.helper.write_code_line(2, 'self._id = self._generate_id()  # Automatically assign a unique id to each instance')
        self.helper.write_code_line(2, f"self._children: List['{component_class_name}'] = []  # Private children property")
        self.helper.write_code_line(2, 'self.name = name')
        self.helper.write_code_line(2, f'self._validator = {validator_class_name}(self)  # Initialize the validator with the current component instance')
        self.helper.write_empty_line()

    def write___hash___method(self):
        # Not included in target example, write pass
        self.helper.write_code_line(1, 'def __hash__(self):')
        self.helper.write_code_line(2, 'pass')
        self.helper.write_empty_line()

    def write___str___method(self):
        # Not included in target example, write pass
        self.helper.write_code_line(1, 'def __str__(self):')
        self.helper.write_code_line(2, 'pass')
        self.helper.write_empty_line()

    def write__ensure_tuple_method(self):
        # Implemented in target example
        self.helper.write_code_line(1, '@classmethod')
        self.helper.write_code_line(1, 'def _ensure_tuple(cls, args: Union[tuple, Any]) -> tuple:')
        self.helper.write_code_line(2, 'if isinstance(args, tuple):')
        self.helper.write_code_line(3, 'return args')
        self.helper.write_code_line(2, 'return (args,)')
        self.helper.write_empty_line()

    def write__generate_id_method(self):
        # Implemented in target example
        self.helper.write_code_line(1, '@classmethod')
        self.helper.write_code_line(1, 'def _generate_id(cls) -> int:')
        self.helper.write_code_line(2, '"""Generates a new unique id for each instance."""')
        self.helper.write_code_line(2, 'cls._id_counter += 1')
        self.helper.write_code_line(2, 'return cls._id_counter')
        self.helper.write_empty_line()

    def write_any_bool_methods(self):
        # Generate methods for boolean properties that start with 'is_'
        for prop_name, prop_value in self.leaf_properties.items():
            if isinstance(prop_value, bool) and prop_name.startswith('is_'):
                method_name = f'any_{prop_name[3:]}'
                self.helper.write_code_line(1, f'def {method_name}(self) -> bool:')
                self.helper.write_code_line(2, f'"""Dummy implementation for method {method_name}."""')
                self.helper.write_code_line(2, '# Assuming that this is a method returning False for now.')
                self.helper.write_code_line(2, 'return False')
                self.helper.write_empty_line()

    def write__validate_composite_logic_method(self):
        # Not included in target example, write pass
        self.helper.write_code_line(1, 'def _validate_composite_logic(self):')
        self.helper.write_code_line(2, 'pass')
        self.helper.write_empty_line()

    def write__validate_remove_logic_method(self):
        # Not included in target example, write pass
        self.helper.write_code_line(1, 'def _validate_remove_logic(self):')
        self.helper.write_code_line(2, 'pass')
        self.helper.write_empty_line()

    def write_validate_structure_method(self):
        # Implemented in target example
        self.helper.write_code_line(1, 'def validate_structure(self,')
        self.helper.write_code_line(2, 'no_circular_references: bool = True,')
        self.helper.write_code_line(2, 'no_parent_duplication_conflict: bool = True,')
        self.helper.write_code_line(2, 'parent_child_relationships_are_consistent: bool = True,')
        self.helper.write_code_line(2, 'only_component_objects_in_composites: bool = True,')
        self.helper.write_code_line(2, 'all_parents_are_composites: bool = True,')
        self.helper.write_code_line(2, 'leaf_has_no_children: bool = True,')
        self.helper.write_code_line(2, 'components_are_unique: bool = True,')
        self.helper.write_code_line(2, 'ids_are_unique: bool = True,')
        self.helper.write_code_line(2, 'names_are_unique: bool = True,')
        self.helper.write_code_line(2, 'all_composites_use_deny_policy: bool = False,')
        self.helper.write_code_line(2, 'max_one_parent: bool = True,')
        self.helper.write_code_line(2, 'condition_func_in_all_conditional_composites: bool = True')
        self.helper.write_code_line(1, ') -> None:')
        self.helper.write_code_line(2, '"""')
        self.helper.write_code_line(2, 'Validates the structure of the component by delegating to the Validator.')
        self.helper.write_code_line(2, '')
        self.helper.write_code_line(2, 'Each validation can be individually toggled on or off using boolean flags.')
        self.helper.write_code_line(2, 'Setting any flag to `False` will skip that specific validation.')
        self.helper.write_code_line(2, '')
        self.helper.write_code_line(2, 'Raises:')
        self.helper.write_code_line(2, '    ValueError: If any validation fails.')
        self.helper.write_code_line(2, '"""')
        self.helper.write_code_line(2, 'self._validator.validate_structure(')
        self.helper.write_code_line(3, 'no_circular_references=no_circular_references,')
        self.helper.write_code_line(3, 'no_parent_duplication_conflict=no_parent_duplication_conflict,')
        self.helper.write_code_line(3, 'parent_child_relationships_are_consistent=parent_child_relationships_are_consistent,')
        self.helper.write_code_line(3, 'only_component_objects_in_composites=only_component_objects_in_composites,')
        self.helper.write_code_line(3, 'all_parents_are_composites=all_parents_are_composites,')
        self.helper.write_code_line(3, 'leaf_has_no_children=leaf_has_no_children,')
        self.helper.write_code_line(3, 'components_are_unique=components_are_unique,')
        self.helper.write_code_line(3, 'ids_are_unique=ids_are_unique,')
        self.helper.write_code_line(3, 'names_are_unique=names_are_unique,')
        self.helper.write_code_line(3, 'all_composites_use_deny_policy=all_composites_use_deny_policy,')
        self.helper.write_code_line(3, 'max_one_parent=max_one_parent,')
        self.helper.write_code_line(3, 'condition_func_in_all_conditional_composites=condition_func_in_all_conditional_composites')
        self.helper.write_code_line(2, ')')
        self.helper.write_empty_line()

    def write_add_method(self):
        # Abstract method
        component_class_name = self._get_component_class_name()
        self.helper.write_code_line(1, '@abstractmethod')
        self.helper.write_code_line(1, f'def add(self, component: \'{component_class_name}\') -> None:')
        self.helper.write_code_line(2, '"""Adds a child component."""')
        self.helper.write_code_line(2, 'pass')
        self.helper.write_empty_line()

    def write_remove_method(self):
        # Abstract method
        component_class_name = self._get_component_class_name()
        self.helper.write_code_line(1, '@abstractmethod')
        self.helper.write_code_line(1, f'def remove(self, component: \'{component_class_name}\') -> None:')
        self.helper.write_code_line(2, '"""Removes a child component."""')
        self.helper.write_code_line(2, 'pass')
        self.helper.write_empty_line()

    def write_is_composite_method(self):
        # Implemented in target example
        self.helper.write_code_line(1, 'def is_composite(self) -> bool:')
        self.helper.write_code_line(2, '"""Returns True if this component is a composite."""')
        self.helper.write_code_line(2, 'return bool(self.get_children())')
        self.helper.write_empty_line()

    def write_get_children_method(self):
        # Implemented in target example
        component_class_name = self._get_component_class_name()
        self.helper.write_code_line(1, f'def get_children(self) -> List[\'{component_class_name}\']:')
        self.helper.write_code_line(2, '"""Get the list of children for this component."""')
        self.helper.write_code_line(2, 'return self._children')
        self.helper.write_empty_line()

    def write_remove_components_recursively_method(self):
        # Implemented in target example
        self.helper.write_code_line(1, 'def remove_components_recursively(self) -> None:')
        self.helper.write_code_line(2, '"""Recursively remove components."""')
        self.helper.write_code_line(2, 'for child in self.get_children():')
        self.helper.write_code_line(3, 'child.remove_components_recursively()')
        self.helper.write_code_line(2, 'self._children.clear()')
        self.helper.write_empty_line()

    def write_get_components_recursively_method(self):
        # Implemented in target example
        component_class_name = self._get_component_class_name()
        self.helper.write_code_line(1, f'def get_components_recursively(self) -> List[\'{component_class_name}\']:')
        self.helper.write_code_line(2, '"""Recursively gather all components."""')
        self.helper.write_code_line(2, 'components = [self]')
        self.helper.write_code_line(2, 'for child in self.get_children():')
        self.helper.write_code_line(3, 'components.extend(child.get_components_recursively())')
        self.helper.write_code_line(2, 'return components')
        self.helper.write_empty_line()

    def write_execute_operation_recursively_method(self):
        # Implemented in target example
        component_class_name = self._get_component_class_name()
        self.helper.write_code_line(1, f'def execute_operation_recursively(self, operation: Callable[[\'{component_class_name}\'], None]) -> None:')
        self.helper.write_code_line(2, '"""Recursively execute an operation on this component and all its children."""')
        self.helper.write_code_line(2, 'operation(self)')
        self.helper.write_code_line(2, 'for child in self.get_children():')
        self.helper.write_code_line(3, 'child.execute_operation_recursively(operation)')
        self.helper.write_empty_line()

    def write_get_structure_as_dict_method(self):
        # Abstract method
        self.helper.write_code_line(1, '@abstractmethod')
        self.helper.write_code_line(1, 'def get_structure_as_dict(self) -> Dict:')
        self.helper.write_code_line(2, '"""Returns a dictionary representation of the component structure."""')
        self.helper.write_code_line(2, 'pass')
        self.helper.write_empty_line()

    def write_is_leaf_method(self):
        # Implemented in target example
        self.helper.write_code_line(1, 'def is_leaf(self) -> bool:')
        self.helper.write_code_line(2, '"""Returns True if this component is a leaf node."""')
        self.helper.write_code_line(2, 'return not self.get_children()')
        self.helper.write_empty_line()

    def write_id_method(self):
        # Implemented in target example
        self.helper.write_code_line(1, '@property')
        self.helper.write_code_line(1, 'def id(self) -> int:')
        self.helper.write_code_line(2, 'return self._id')
        self.helper.write_empty_line()

    def write_calculate_depth_method(self):
        # Implemented in target example
        self.helper.write_code_line(1, 'def calculate_depth(self) -> int:')
        self.helper.write_code_line(2, '"""Calculate the depth of the component tree."""')
        self.helper.write_code_line(2, 'if not self.get_children():')
        self.helper.write_code_line(3, 'return 1')
        self.helper.write_code_line(2, 'return 1 + max(child.calculate_depth() for child in self.get_children())')
        self.helper.write_empty_line()

    def write_get_parents_method(self):
        # Implemented in target example
        component_class_name = self._get_component_class_name()
        self.helper.write_code_line(1, f'def get_parents(self) -> List[\'{component_class_name}\']:')
        self.helper.write_code_line(2, '"""Get the list of parents for this component."""')
        self.helper.write_code_line(2, 'return self._parents')
        self.helper.write_empty_line()

    def write_clone_method(self):
        # Implemented in target example
        component_class_name = self._get_component_class_name()
        self.helper.write_code_line(1, f'def clone(self) -> \'{component_class_name}\':')
        self.helper.write_code_line(2, '"""Create a step-by-step clone of this component, assigning a new ID to the clone and its children."""')
        self.helper.write_code_line(2, 'cloned_component = self.__class__.__new__(self.__class__)')
        self.helper.write_empty_line()
        self.helper.write_code_line(2, 'for attr_name, attr_value in self.__dict__.items():')
        self.helper.write_code_line(3, 'if attr_name == \'_id\':')
        self.helper.write_code_line(4, 'setattr(cloned_component, \'_id\', self._generate_id())')
        self.helper.write_code_line(3, 'else:')
        self.helper.write_code_line(4, 'setattr(cloned_component, attr_name, attr_value)')
        self.helper.write_empty_line()
        self.helper.write_code_line(2, 'cloned_component._children = []')
        self.helper.write_code_line(2, 'for child in self.get_children():')
        self.helper.write_code_line(3, 'cloned_child = child.clone()')
        self.helper.write_code_line(3, 'cloned_component.add(cloned_child)')
        self.helper.write_empty_line()
        self.helper.write_code_line(2, 'cloned_component._parents = []')
        self.helper.write_empty_line()
        self.helper.write_code_line(2, 'return cloned_component')
        self.helper.write_empty_line()

    def write__undo_add_method(self):
        # Not included in target example, write pass
        self.helper.write_code_line(1, 'def _undo_add(self):')
        self.helper.write_code_line(2, 'pass')
        self.helper.write_empty_line()

    def write__undo_remove_method(self):
        # Not included in target example, write pass
        self.helper.write_code_line(1, 'def _undo_remove(self):')
        self.helper.write_code_line(2, 'pass')
        self.helper.write_empty_line()

    def write_export_to_pickle_method(self):
        # Implemented in target example
        self.helper.write_code_line(1, 'def export_to_pickle(self, path: str) -> None:')
        self.helper.write_code_line(2, '"""Exports the component structure to a pickle file."""')
        self.helper.write_code_line(2, 'self._loader.export_to_pickle(self, path)')
        self.helper.write_empty_line()

    def write_import_from_pickle_method(self):
        # Implemented in target example
        component_class_name = self._get_component_class_name()
        self.helper.write_code_line(1, '@classmethod')
        self.helper.write_code_line(1, f'def import_from_pickle(cls, path: str) -> \'{component_class_name}\':')
        self.helper.write_code_line(2, '"""Imports a component structure from a pickle file."""')
        self.helper.write_code_line(2, 'return cls._loader.import_from_pickle(path)')
        self.helper.write_empty_line()

    # Helper methods to avoid using specific values from project_structure
    def _get_component_class_name(self):
        # Use the key 'component' capitalized
        return self.project_structure.get('component', 'Component').capitalize()

    def _get_component_name_snake(self):
        # Convert the key 'component' to snake_case
        component_name = self.project_structure.get('component', 'component')
        return Helper.convert_to_snake_case(component_name)

    def _get_component_module_path(self):
        # Return the module path for the component
        component_name_snake = self._get_component_name_snake()
        return f"{component_name_snake}.abstract.{component_name_snake}"

    def save_file(self):
        self.helper.save()
