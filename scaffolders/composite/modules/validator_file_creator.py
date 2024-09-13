from modules.helpers.helper import Helper

class ValidatorFileCreator:
    def __init__(self, filename, root_module=None):
        self.filename = filename
        self.helper = Helper(filename, root_module)

    def create_validator_file(self, project_structure):
        component_name = project_structure['component']
        self._write_imports(component_name)
        self._write_class_definition(component_name)
        self._write_init_method(component_name)
        self._write_validate_structure_method(component_name)
        self._write_private_validation_methods(component_name)
        self.helper.save()

    def _write_imports(self, component_name):
        # Write the import lines at the top of the file
        self.helper.write_code_line(0, 'from typing import Set')
        self.helper.write_empty_line()

    def _write_class_definition(self, component_name):
        # Write the class definition for the validator
        self.helper.write_code_line(0, f'class {component_name}Validator:')
        self.helper.write_code_line(1, '"""')
        self.helper.write_code_line(1, f'Responsible for validating the structure of {component_name} components recursively from the root.')
        self.helper.write_code_line(1, '"""')
        self.helper.write_empty_line()

    def _write_init_method(self, component_name):
        # Write the __init__ method to initialize the validator with the component
        self.helper.write_code_line(1, 'def __init__(self, component):')
        self.helper.write_code_line(2, 'self.component = component')
        self.helper.write_empty_line()

    def _write_validate_structure_method(self, component_name):
        # Write the validate_structure method
        composite_key = Helper.convert_to_snake_case(project_structure.get('composite', 'composite'))
        self.helper.write_code_line(1, 'def validate_structure(self,')
        self.helper.write_code_line(2, 'no_circular_references: bool = True,')
        self.helper.write_code_line(2, 'no_parent_duplication_conflict: bool = True,')
        self.helper.write_code_line(2, 'parent_child_relationships_are_consistent: bool = True,')
        self.helper.write_code_line(2, f'only_{component_name.lower()}_objects_in_{composite_key}: bool = True,')
        self.helper.write_code_line(2, f'all_parents_are_{composite_key}s: bool = True,')
        self.helper.write_code_line(2, 'leaf_has_no_children: bool = True,')
        self.helper.write_code_line(2, 'components_are_unique: bool = True,')
        self.helper.write_code_line(2, 'ids_are_unique: bool = True,')
        self.helper.write_code_line(2, 'names_are_unique: bool = True,')
        self.helper.write_code_line(2, f'all_{composite_key}s_use_deny_policy: bool = True,')
        self.helper.write_code_line(2, 'max_one_parent: bool = True,')
        self.helper.write_code_line(2, f'condition_func_in_all_conditional_{composite_key}s: bool = True')
        self.helper.write_code_line(1, ') -> None:')
        self.helper.write_code_line(2, '"""Recursively validates the structure of the component starting from the root."""')
        self.helper.write_empty_line()

        # Write validation checks inside the validate_structure method
        validation_checks = [
            'no_circular_references',
            'no_parent_duplication_conflict',
            'parent_child_relationships_are_consistent',
            f'only_{component_name.lower()}_objects_in_{composite_key}',
            f'all_parents_are_{composite_key}s',
            'leaf_has_no_children',
            'components_are_unique',
            'ids_are_unique',
            'names_are_unique',
            f'all_{composite_key}s_use_deny_policy',
            'max_one_parent',
            f'condition_func_in_all_conditional_{composite_key}s',
        ]

        for check in validation_checks:
            self.helper.write_code_line(2, f'if {check}:')
            method_name = self._convert_validation_name(check)
            self.helper.write_code_line(3, f'self.{method_name}()')

        self.helper.write_empty_line()

    def _write_private_validation_methods(self, component_name):
        composite_name = Helper.convert_to_snake_case(project_structure.get('composite', 'composite'))

        private_methods = {
            '_validate_no_circular_references': 'Check recursively for circular references.',
            '_validate_no_parent_duplication_conflict': 'Validate that no component has multiple parents.',
            '_validate_parent_child_relationships': 'Ensure parent-child relationships are consistent.',
            f'_validate_only_{component_name.lower()}_objects_in_{composite_name}': 'Check that only component objects exist within the composite.',
            f'_validate_all_parents_are_{composite_name}s': f'Ensure all parents of a component are {composite_name} objects.',
            '_validate_leaf_has_no_children': 'Ensure leaf components do not have children.',
            '_validate_components_unique': 'Check if all components are unique.',
            '_validate_ids_unique': 'Ensure all component ids are unique.',
            '_validate_names_unique': 'Ensure all component names are unique.',
            f'_validate_all_{composite_name}s_use_deny_policy': f'Ensure all {composite_name}s use the DENY_MULTIPLE_PARENTS policy.',
            '_validate_max_one_parent': 'Ensure each component has at most one parent.',
            f'_validate_condition_func_in_conditional_{composite_name}s': f'Ensure all {composite_name}s with ALLOW_NEW_PARENT_IF have a condition_func defined.'
        }

        for method_name, description in private_methods.items():
            self.helper.write_code_line(1, f'def {method_name}(self):')
            self.helper.write_code_line(2, f'"""{description}"""')
            self.helper.write_code_line(2, 'pass')
            self.helper.write_empty_line()

        # Write helper methods
        self._write_helper_methods(component_name)

    def _write_helper_methods(self, component_name):
        composite_name = Helper.convert_to_snake_case(project_structure.get('composite', 'composite'))

        # _is_composite_instance helper method
        self.helper.write_code_line(1, 'def _is_composite_instance(self, component):')
        self.helper.write_code_line(2, f'from {Helper.convert_to_snake_case(component_name)}.components.composite.{composite_name} import {self.project_structure["composite"]}')
        self.helper.write_code_line(2, f'return isinstance(component, {self.project_structure["composite"]})')
        self.helper.write_empty_line()

        # _is_leaf_instance helper method
        self.helper.write_code_line(1, 'def _is_leaf_instance(self, component):')
        self.helper.write_code_line(2, f'from {Helper.convert_to_snake_case(component_name)}.components.leaves.abstract.leaf import Leaf')
        self.helper.write_code_line(2, 'return isinstance(component, Leaf)')
        self.helper.write_empty_line()

        # _get_duplicate_policy helper method
        self.helper.write_code_line(1, 'def _get_duplicate_policy(self):')
        self.helper.write_code_line(2, f'from {Helper.convert_to_snake_case(component_name)}.components.composite.{composite_name} import {self.project_structure["composite"]}')
        self.helper.write_code_line(2, f'return {self.project_structure["composite"]}.DuplicatePolicy')
        self.helper.write_empty_line()

    def _convert_validation_name(self, check_name):
        return f'_validate_{check_name}'

