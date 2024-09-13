from modules.helpers.component_file_builder.builders.abstract.component_file_builder import ComponentFileBuilder
from modules.helpers.helper import Helper

class CompositeComponentFileBuilder(ComponentFileBuilder):
    def __init__(self, filename, project_structure, root_module=None):
        super().__init__(filename, project_structure, root_module)
        self.project_structure = project_structure
        self.helper = Helper(filename, root_module)
        self.root_module = root_module
        self.leaf_properties = project_structure.get('leaf_properties', {})

    def write___init___method(self):
        # Import statements
        self.helper.write_code_line(0, 'from enum import Enum')
        self.helper.write_code_line(0, 'from typing import Callable, List, Optional, Any, Dict, Union')
        self.helper.write_empty_line()

        # Project-specific imports
        component_module = self._get_component_module_path()
        component_class_name = self._get_component_class_name()
        self.helper.write_import_line(component_module, component_class_name)
        self.helper.write_empty_line()

        # Class definition
        composite_class_name = self._get_composite_class_name()
        self.helper.write_code_line(0, f'class {composite_class_name}({component_class_name}):')

        # Nested DuplicatePolicy Enum
        self.helper.write_code_line(1, 'class DuplicatePolicy(Enum):')
        self.helper.write_code_line(2, 'ALLOW_MULTIPLE_PARENTS = "ALLOW_MULTIPLE_PARENTS"')
        self.helper.write_code_line(2, 'DENY_MULTIPLE_PARENTS = "DENY_MULTIPLE_PARENTS"')
        self.helper.write_code_line(2, 'ALLOW_NEW_PARENT_IF = "ALLOW_NEW_PARENT_IF"')
        self.helper.write_empty_line()

        # Class variable validation_settings
        self.helper.write_code_line(1, '# Class variable to store validation settings, applied to all instances')
        self.helper.write_code_line(1, 'validation_settings: Dict[str, bool] = {')
        validation_keys = [
            'no_circular_references',
            'no_parent_duplication_conflict',
            'parent_child_relationships_are_consistent',
            'only_component_objects_in_composites',
            'all_parents_are_composites',
            'leaf_has_no_children',
            'components_are_unique',
            'ids_are_unique',
            'names_are_unique',
            'all_composites_use_deny_policy',
            'max_one_parent',
            'condition_func_in_all_conditional_composites'
        ]
        for key in validation_keys:
            self.helper.write_code_line(2, f"'{key}': True,")
        self.helper.write_code_line(1, '}')
        self.helper.write_empty_line()

        # __init__ method
        self.helper.write_code_line(1, 'def __init__(')
        self.helper.write_code_line(2, 'self, name: str,')
        self.helper.write_code_line(2, f'duplicate_policy: Optional["{composite_class_name}.DuplicatePolicy"] = None,')
        self.helper.write_code_line(2, f'condition_func: Optional[Callable[[{component_class_name}, {component_class_name}], bool]] = None')
        self.helper.write_code_line(1, '):')
        self.helper.write_code_line(2, '"""')
        self.helper.write_code_line(2, ':param name: Name of the composite.')
        self.helper.write_code_line(2, ':param duplicate_policy: Enum value determining if duplicate parents are allowed.')
        self.helper.write_code_line(2, ':param condition_func: Function to check if component can have multiple parents under certain conditions.')
        self.helper.write_code_line(2, '                       Only required if using ALLOW_NEW_PARENT_IF.')
        self.helper.write_code_line(2, '"""')
        self.helper.write_code_line(2, 'super().__init__(name)  # Pass the name to the base component class constructor')
        self.helper.write_code_line(2, 'self.duplicate_policy = duplicate_policy or self.DuplicatePolicy.DENY_MULTIPLE_PARENTS')
        self.helper.write_code_line(2, 'self.condition_func = condition_func')
        self.helper.write_empty_line()
        self.helper.write_code_line(2, 'if self.duplicate_policy == self.DuplicatePolicy.ALLOW_NEW_PARENT_IF and not self.condition_func:')
        self.helper.write_code_line(3, 'raise ValueError("You must provide a condition_func when using ALLOW_NEW_PARENT_IF policy.")')
        self.helper.write_empty_line()

    def write___hash___method(self):
        self.helper.write_code_line(1, 'def __hash__(self):')
        self.helper.write_code_line(2, 'return super().__hash__()')
        self.helper.write_empty_line()

    def write___str___method(self):
        self.helper.write_code_line(1, 'def __str__(self, level=0) -> str:')
        self.helper.write_code_line(2, 'indent = "    " * level')
        self.helper.write_code_line(2, 'result = f"{indent}{self.name}/\\n"')
        self.helper.write_code_line(2, 'for i, child in enumerate(self.get_children()):')
        self.helper.write_code_line(3, 'connector = "├── " if i < len(self.get_children()) - 1 else "└── "')
        self.helper.write_code_line(3, 'child_str = child.__str__(level + 1)')
        self.helper.write_code_line(3, 'result += f"{indent}{connector}{child_str.strip()}\\n"')
        self.helper.write_code_line(2, 'return result')
        self.helper.write_empty_line()

    def write__ensure_tuple_method(self):
        # Not included in the target file, write as pass
        self.helper.write_code_line(1, 'def _ensure_tuple(self, args):')
        self.helper.write_code_line(2, 'pass')
        self.helper.write_empty_line()

    def write__generate_id_method(self):
        # Not included in the target file, write as pass
        self.helper.write_code_line(1, 'def _generate_id(self):')
        self.helper.write_code_line(2, 'pass')
        self.helper.write_empty_line()

    def write_any_bool_methods(self):
        for prop_name, prop_value in self.leaf_properties.items():
            if isinstance(prop_value, bool) and prop_name.startswith('is_'):
                method_name = f'any_{prop_name[3:]}'
                self.helper.write_code_line(1, f'def {method_name}(self) -> bool:')
                self.helper.write_code_line(2, f'return any(child.{method_name}() for child in self.get_children())')
                self.helper.write_empty_line()

    def write__validate_composite_logic_method(self):
        component_class_name = self._get_component_class_name()
        composite_class_name = self._get_composite_class_name()
        self.helper.write_code_line(1, f'def _validate_composite_logic(self, component: {component_class_name}) -> None:')
        self.helper.write_code_line(2, '"""')
        self.helper.write_code_line(2, 'Perform duplicate parent checks and other composite-level validations based on policies.')
        self.helper.write_code_line(2, '"""')
        self.helper.write_code_line(2, '# Check the policies of all existing parents (composites) of the component')
        self.helper.write_code_line(2, 'for parent in component.get_parents():')
        self.helper.write_code_line(3, f'if parent.duplicate_policy == {composite_class_name}.DuplicatePolicy.DENY_MULTIPLE_PARENTS:')
        self.helper.write_code_line(4, 'raise ValueError(f"Error: {parent.name} has the policy DENY_MULTIPLE_PARENTS, "')
        self.helper.write_code_line(5, '                     "which denies adding multiple parents.")')
        self.helper.write_empty_line()
        self.helper.write_code_line(3, f'if parent.duplicate_policy == {composite_class_name}.DuplicatePolicy.ALLOW_NEW_PARENT_IF:')
        self.helper.write_code_line(4, 'if not parent.condition_func or not parent.condition_func(parent, component):')
        # Corrected line with escaped curly braces
        self.helper.write_code_line(5, 'raise ValueError(f"Error: Condition for adding {{component.name}} to {{parent.name}} was not satisfied.")')
        self.helper.write_empty_line()
        self.helper.write_code_line(2, '# Check the policy of the current composite (self)')
        self.helper.write_code_line(2, 'if self.duplicate_policy == self.DuplicatePolicy.DENY_MULTIPLE_PARENTS and component.get_parents():')
        self.helper.write_code_line(3, 'raise ValueError(f"Error: {self.name} has the policy DENY_MULTIPLE_PARENTS, "')
        self.helper.write_code_line(4, '                     "and this component already has a parent.")')
        self.helper.write_empty_line()
        self.helper.write_code_line(2, 'if self.duplicate_policy == self.DuplicatePolicy.ALLOW_NEW_PARENT_IF:')
        self.helper.write_code_line(3, 'if not self.condition_func or not self.condition_func(self, component):')
        # Corrected line with escaped curly braces
        self.helper.write_code_line(4, 'raise ValueError(f"Error: Condition for adding {{component.name}} to {{self.name}} was not satisfied.")')
        self.helper.write_empty_line()

    def write__validate_remove_logic_method(self):
        component_class_name = self._get_component_class_name()
        self.helper.write_code_line(1, f'def _validate_remove_logic(self, component: {component_class_name}) -> None:')
        self.helper.write_code_line(2, '"""')
        self.helper.write_code_line(2, 'Validation logic specifically for remove operation. Skips checks for multiple parents.')
        self.helper.write_code_line(2, '"""')
        self.helper.write_code_line(2, 'if component not in self.get_children():')
        self.helper.write_code_line(3, 'raise ValueError(f"Error: {component.name} is not a child of {self.name}, cannot remove.")')
        self.helper.write_empty_line()

    def write_validate_structure_method(self):
        composite_class_name = self._get_composite_class_name()
        self.helper.write_code_line(1, 'def validate_structure(self) -> None:')
        self.helper.write_code_line(2, '"""')
        self.helper.write_code_line(2, 'Validate the structure of the component using class-level validation settings.')
        self.helper.write_code_line(2, '"""')
        self.helper.write_code_line(2, f'self._validator.validate_structure(**{composite_class_name}.validation_settings)')
        self.helper.write_empty_line()

    def write_add_method(self):
        component_class_name = self._get_component_class_name()
        self.helper.write_code_line(1, f'def add(self, component: {component_class_name}) -> None:')
        self.helper.write_code_line(2, '# Perform composite-level validation logic before adding')
        self.helper.write_code_line(2, 'self._validate_composite_logic(component)')
        self.helper.write_empty_line()
        self.helper.write_code_line(2, '# Add the component to this composite')
        self.helper.write_code_line(2, 'component._parents.append(self)  # Add the current composite to the parents')
        self.helper.write_code_line(2, 'self._children.append(component)')
        self.helper.write_empty_line()
        self.helper.write_code_line(2, '# Perform validation using class-level validation settings')
        self.helper.write_code_line(2, 'try:')
        self.helper.write_code_line(3, 'self.validate_structure()  # Validate using class-level settings')
        self.helper.write_code_line(2, 'except Exception as validation_error:')
        self.helper.write_code_line(3, '# Rollback the add operation')
        self.helper.write_code_line(3, 'self._undo_add(component)')
        self.helper.write_code_line(3, 'raise ValueError(f"Error adding {component.name} to {self.name}: Validation failed: {str(validation_error)}")')
        self.helper.write_empty_line()

    def write_remove_method(self):
        component_class_name = self._get_component_class_name()
        self.helper.write_code_line(1, f'def remove(self, component: {component_class_name}) -> None:')
        self.helper.write_code_line(2, '# Perform composite-level validation logic before removing')
        self.helper.write_code_line(2, 'self._validate_remove_logic(component)')
        self.helper.write_empty_line()
        self.helper.write_code_line(2, '# Remove the component if it exists in this composite')
        self.helper.write_code_line(2, 'if component in self.get_children():')
        self.helper.write_code_line(3, 'component._parents.remove(self)  # Remove this composite from the component\'s parents')
        self.helper.write_code_line(3, 'self._children.remove(component)')
        self.helper.write_empty_line()
        self.helper.write_code_line(2, '# Perform validation after removing')
        self.helper.write_code_line(2, 'try:')
        self.helper.write_code_line(3, 'self.validate_structure()  # Validate using class-level settings')
        self.helper.write_code_line(2, 'except Exception as validation_error:')
        self.helper.write_code_line(3, '# Rollback the remove operation')
        self.helper.write_code_line(3, 'self._undo_remove(component)')
        self.helper.write_code_line(3, 'raise ValueError(f"Error removing {component.name} from {self.name}: Validation failed: {str(validation_error)}")')
        self.helper.write_empty_line()

    def write_is_composite_method(self):
        self.helper.write_code_line(1, 'def is_composite(self) -> bool:')
        self.helper.write_code_line(2, 'return True')
        self.helper.write_empty_line()

    def write_get_children_method(self):
        # Not included in the target file, write as pass
        self.helper.write_code_line(1, 'def get_children(self):')
        self.helper.write_code_line(2, 'pass')
        self.helper.write_empty_line()

    def write_remove_components_recursively_method(self):
        component_class_name = self._get_component_class_name()
        composite_class_name = self._get_composite_class_name()
        self.helper.write_code_line(1, f'def remove_components_recursively(')
        self.helper.write_code_line(2, 'self,')
        self.helper.write_code_line(2, f'condition_func: Optional[Callable[[{component_class_name}, Any], bool]] = None,')
        self.helper.write_code_line(2, 'condition_args: Union[tuple, Any] = ()')
        self.helper.write_code_line(1, f') -> List[{component_class_name}]:')
        self.helper.write_code_line(2, 'condition_args = self._ensure_tuple(condition_args)')
        self.helper.write_code_line(2, 'removed_components = []')
        self.helper.write_empty_line()
        self.helper.write_code_line(2, 'for child in self.get_children()[:]:')
        self.helper.write_code_line(3, f'# If the child is a {composite_class_name}, recursively remove components')
        self.helper.write_code_line(3, f'if isinstance(child, {composite_class_name}):')
        self.helper.write_code_line(4, 'removed_components.extend(child.remove_components_recursively(condition_func, condition_args))')
        self.helper.write_empty_line()
        self.helper.write_code_line(3, '# If no condition_func is provided, remove the component, otherwise check the condition')
        self.helper.write_code_line(3, 'if condition_func is None or condition_func(child, *condition_args):')
        self.helper.write_code_line(4, 'child._parents.remove(self)  # Remove this composite as parent before removing')
        self.helper.write_code_line(4, 'self._children.remove(child)')
        self.helper.write_code_line(4, 'removed_components.append(child)')
        self.helper.write_empty_line()
        self.helper.write_code_line(2, 'return removed_components')
        self.helper.write_empty_line()

    def write_get_components_recursively_method(self):
        component_class_name = self._get_component_class_name()
        self.helper.write_code_line(1, f'def get_components_recursively(')
        self.helper.write_code_line(2, 'self,')
        self.helper.write_code_line(2, f'condition_func: Optional[Callable[[{component_class_name}, Any], bool]] = None,')
        self.helper.write_code_line(2, 'condition_args: Union[tuple, Any] = (),')
        self.helper.write_code_line(1, f') -> List[{component_class_name}]:')
        self.helper.write_code_line(2, 'condition_args = self._ensure_tuple(condition_args)')
        self.helper.write_code_line(2, 'matching_components = []  # Initialize an empty list')
        self.helper.write_empty_line()
        self.helper.write_code_line(2, '# Check if the current component (self) matches the condition and should be included')
        self.helper.write_code_line(2, 'if condition_func is None or condition_func(self, *condition_args):')
        self.helper.write_code_line(3, 'matching_components.append(self)')
        self.helper.write_empty_line()
        self.helper.write_code_line(2, '# Recursively check children')
        self.helper.write_code_line(2, 'for child in self.get_children():')
        self.helper.write_code_line(3, 'matching_components.extend(')
        self.helper.write_code_line(4, 'child.get_components_recursively(condition_func=condition_func, condition_args=condition_args)')
        self.helper.write_code_line(3, ')')
        self.helper.write_empty_line()
        self.helper.write_code_line(2, 'return matching_components')
        self.helper.write_empty_line()

    def write_execute_operation_recursively_method(self):
        component_class_name = self._get_component_class_name()
        self.helper.write_code_line(1, f'def execute_operation_recursively(')
        self.helper.write_code_line(2, 'self,')
        self.helper.write_code_line(2, f'operation_func: Callable[[{component_class_name}, Any], Any],')
        self.helper.write_code_line(2, 'operation_args: Union[tuple, Any] = (),')
        self.helper.write_code_line(2, f'condition_func: Optional[Callable[[{component_class_name}, Any], bool]] = None,')
        self.helper.write_code_line(2, 'condition_args: Union[tuple, Any] = (),')
        self.helper.write_code_line(1, ') -> List[Any]:')
        self.helper.write_code_line(2, 'operation_args = self._ensure_tuple(operation_args)')
        self.helper.write_code_line(2, 'condition_args = self._ensure_tuple(condition_args)')
        self.helper.write_code_line(2, 'results = []')
        self.helper.write_empty_line()
        self.helper.write_code_line(2, '# Apply the operation to the composite itself if the condition is satisfied or no condition is provided')
        self.helper.write_code_line(2, 'if condition_func is None or condition_func(self, *condition_args):')
        self.helper.write_code_line(3, 'result = operation_func(self, *operation_args)')
        self.helper.write_code_line(3, 'results.append(result)')
        self.helper.write_empty_line()
        self.helper.write_code_line(2, '# Recursively apply the operation to children')
        self.helper.write_code_line(2, 'for child in self.get_children():')
        self.helper.write_code_line(3, 'results.extend(')
        self.helper.write_code_line(4, 'child.execute_operation_recursively(')
        self.helper.write_code_line(5, 'operation_func=operation_func,')
        self.helper.write_code_line(5, 'operation_args=operation_args,')
        self.helper.write_code_line(5, 'condition_func=condition_func,')
        self.helper.write_code_line(5, 'condition_args=condition_args,')
        self.helper.write_code_line(4, ')')
        self.helper.write_code_line(3, ')')
        self.helper.write_empty_line()
        self.helper.write_code_line(2, 'return results')
        self.helper.write_empty_line()

    def write_get_structure_as_dict_method(self):
        self.helper.write_code_line(1, 'def get_structure_as_dict(self) -> Dict:')
        self.helper.write_code_line(2, 'structure = {self.name: {}}')
        self.helper.write_code_line(2, 'for child in self.get_children():')
        self.helper.write_code_line(3, 'structure[self.name].update(child.get_structure_as_dict())')
        self.helper.write_code_line(2, 'return structure')
        self.helper.write_empty_line()

    def write_is_leaf_method(self):
        self.helper.write_code_line(1, 'def is_leaf(self) -> bool:')
        self.helper.write_code_line(2, 'return False')
        self.helper.write_empty_line()

    def write_id_method(self):
        # Not included in the target file, write as pass
        self.helper.write_code_line(1, 'def id(self):')
        self.helper.write_code_line(2, 'pass')
        self.helper.write_empty_line()

    def write_calculate_depth_method(self):
        self.helper.write_code_line(1, 'def calculate_depth(self) -> int:')
        self.helper.write_code_line(2, 'return 1 + max(child.calculate_depth() for child in self.get_children()) if self.get_children() else 1')
        self.helper.write_empty_line()

    def write_get_parents_method(self):
        # Not included in the target file, write as pass
        self.helper.write_code_line(1, 'def get_parents(self):')
        self.helper.write_code_line(2, 'pass')
        self.helper.write_empty_line()

    def write_clone_method(self):
        # Not included in the target file, write as pass
        self.helper.write_code_line(1, 'def clone(self):')
        self.helper.write_code_line(2, 'pass')
        self.helper.write_empty_line()

    def write__undo_add_method(self):
        component_class_name = self._get_component_class_name()
        self.helper.write_code_line(1, f'def _undo_add(self, component: {component_class_name}) -> None:')
        self.helper.write_code_line(2, '"""')
        self.helper.write_code_line(2, 'Rollback the add operation directly by updating _parents and _children.')
        self.helper.write_code_line(2, '"""')
        self.helper.write_code_line(2, 'if component in self.get_children():')
        self.helper.write_code_line(3, 'component._parents.remove(self)')
        self.helper.write_code_line(3, 'self._children.remove(component)')
        self.helper.write_empty_line()

    def write__undo_remove_method(self):
        component_class_name = self._get_component_class_name()
        self.helper.write_code_line(1, f'def _undo_remove(self, component: {component_class_name}) -> None:')
        self.helper.write_code_line(2, '"""')
        self.helper.write_code_line(2, 'Rollback the remove operation directly by updating _parents and _children.')
        self.helper.write_code_line(2, '"""')
        self.helper.write_code_line(2, 'component._parents.append(self)')
        self.helper.write_code_line(2, 'self._children.append(component)')
        self.helper.write_empty_line()

    def write_export_to_pickle_method(self):
        # Not included in the target file, write as pass
        self.helper.write_code_line(1, 'def export_to_pickle(self, path):')
        self.helper.write_code_line(2, 'pass')
        self.helper.write_empty_line()

    def write_import_from_pickle_method(self):
        # Not included in the target file, write as pass
        self.helper.write_code_line(1, 'def import_from_pickle(self, path):')
        self.helper.write_code_line(2, 'pass')
        self.helper.write_empty_line()

    # Helper methods to avoid using specific values from project_structure
    def _get_component_class_name(self):
        return self.project_structure.get('component', 'Component').capitalize()

    def _get_composite_class_name(self):
        return self.project_structure.get('composite', 'Composite').capitalize()

    def _get_component_name_snake(self):
        component_name = self.project_structure.get('component', 'component')
        return Helper.convert_to_snake_case(component_name)

    def _get_component_module_path(self):
        component_name_snake = self._get_component_name_snake()
        return f"{component_name_snake}.abstract.{component_name_snake}"

    def save_file(self):
        self.helper.save()
