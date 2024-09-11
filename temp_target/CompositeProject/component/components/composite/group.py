from enum import Enum
from typing import Callable, List, Optional, Any, Dict, Union
from component.abstract.graphic import Graphic

class Group(Graphic):
    class DuplicatePolicy(Enum):
        ALLOW_MULTIPLE_PARENTS = "ALLOW_MULTIPLE_PARENTS"
        DENY_MULTIPLE_PARENTS = "DENY_MULTIPLE_PARENTS"
        ALLOW_NEW_PARENT_IF = "ALLOW_NEW_PARENT_IF"

    # Class variable to store validation settings, applied to all instances
    validation_settings: Dict[str, bool] = {
        'no_circular_references': True,
        'no_parent_duplication_conflict': True,
        'parent_child_relationships_are_consistent': True,
        'only_graphic_objects_in_groups': True,
        'all_parents_are_groups': True,
        'leaf_has_no_children': True,
        'components_are_unique': True,
        'ids_are_unique': True,
        'names_are_unique': True,
        'all_groups_use_deny_policy': True,
        'max_one_parent': True,
        'condition_func_in_all_conditional_groups': True
    }

    def __init__(self, name: str, 
                 duplicate_policy: Optional['Group.DuplicatePolicy'] = None, 
                 condition_func: Optional[Callable[[Graphic, Graphic], bool]] = None):
        """
        :param name: Name of the group.
        :param duplicate_policy: Enum value determining if duplicate parents are allowed.
        :param condition_func: Function to check if component can have multiple parents under certain conditions.
                               Only required if using ALLOW_NEW_PARENT_IF.
        """
        super().__init__(name)  # Pass the name to the base Graphic class constructor
        self.duplicate_policy = duplicate_policy or Group.DuplicatePolicy.DENY_MULTIPLE_PARENTS
        self.condition_func = condition_func

        if self.duplicate_policy == Group.DuplicatePolicy.ALLOW_NEW_PARENT_IF and not self.condition_func:
            raise ValueError("You must provide a condition_func when using ALLOW_NEW_PARENT_IF policy.")

    def get_structure_as_dict(self) -> Dict:
        structure = {self.name: {}}
        for child in self.get_children():
            structure[self.name].update(child.get_structure_as_dict())
        return structure

    def __str__(self, level=0) -> str:
        indent = "    " * level
        result = f"{indent}{self.name}/\n"
        for i, child in enumerate(self.get_children()):
            connector = "├── " if i < len(self.get_children()) - 1 else "└── "
            child_str = child.__str__(level + 1)
            result += f"{indent}{connector}{child_str.strip()}\n"
        return result

    def __hash__(self):
        return super().__hash__()

    def is_composite(self) -> bool:
        return True

    def is_leaf(self) -> bool:
        return False

    def any_active(self) -> bool:
        return any(child.any_active() for child in self.get_children())

    def get_components_recursively(
        self,
        condition_func: Optional[Callable[[Graphic, Any], bool]] = None,
        condition_args: Union[tuple, Any] = (),
    ) -> List[Graphic]:
        condition_args = self._ensure_tuple(condition_args)
        matching_components = []  # Initialize an empty list

        # Check if the current component (self) matches the condition and should be included
        if condition_func is None or condition_func(self, *condition_args):
            matching_components.append(self)

        # Recursively check children
        for child in self.get_children():
            matching_components.extend(
                child.get_components_recursively(condition_func=condition_func, condition_args=condition_args)
            )

        return matching_components

    def remove_components_recursively(
        self,
        condition_func: Optional[Callable[[Graphic, Any], bool]] = None,
        condition_args: Union[tuple, Any] = ()
    ) -> List[Graphic]:
        condition_args = self._ensure_tuple(condition_args)
        removed_components = []

        for child in self.get_children()[:]:
            # If the child is a Group, recursively remove components
            if isinstance(child, Group):
                removed_components.extend(child.remove_components_recursively(condition_func, condition_args))
            
            # If no condition_func is provided, remove the component, otherwise check the condition
            if condition_func is None or condition_func(child, *condition_args):
                child._parents.remove(self)  # Remove this group as parent before removing
                self._children.remove(child)
                removed_components.append(child)
        
        return removed_components

    def execute_operation_recursively(
        self,
        operation_func: Callable[[Graphic, Any], Any],
        operation_args: Union[tuple, Any] = (),
        condition_func: Optional[Callable[[Graphic, Any], bool]] = None,
        condition_args: Union[tuple, Any] = (),
    ) -> List[Any]:
        operation_args = self._ensure_tuple(operation_args)
        condition_args = self._ensure_tuple(condition_args)
        results = []

        # Apply the operation to the group itself if the condition is satisfied or no condition is provided
        if condition_func is None or condition_func(self, *condition_args):
            result = operation_func(self, *operation_args)
            results.append(result)

        # Recursively apply the operation to children
        for child in self.get_children():
            results.extend(
                child.execute_operation_recursively(
                    operation_func=operation_func,
                    operation_args=operation_args,
                    condition_func=condition_func,
                    condition_args=condition_args,
                )
            )

        return results

    def calculate_depth(self) -> int:
        return 1 + max(child.calculate_depth() for child in self.get_children()) if self.get_children() else 1  # Groups with no children return 1

    def add(self, component: Graphic) -> None:
        # Perform group-level validation logic before adding
        self._validate_group_logic(component)

        # Add the component to this group
        component._parents.append(self)  # Add the current group to the parents
        self._children.append(component)

        # Perform validation using class-level validation settings
        try:
            self.validate_structure()  # Validate using class-level settings
        except Exception as validation_error:
            # Rollback the add operation
            self._undo_add(component)
            raise ValueError(f"Error adding {component.name} to {self.name}: Validation failed: {str(validation_error)}")

    def remove(self, component: Graphic) -> None:
        # Perform group-level validation logic before removing
        self._validate_remove_logic(component)

        # Remove the component if it exists in this group
        if component in self.get_children():
            component._parents.remove(self)  # Remove this group from the component's parents
            self._children.remove(component)

        # Perform validation after removing
        try:
            self.validate_structure()  # Validate using class-level settings
        except Exception as validation_error:
            # Rollback the remove operation
            self._undo_remove(component)
            raise ValueError(f"Error removing {component.name} from {self.name}: Validation failed: {str(validation_error)}")

    def _validate_group_logic(self, component: Graphic) -> None:
        """
        Perform duplicate parent checks and other group-level validations based on policies.
        """
        # Check the policies of all existing parents (groups) of the component
        for parent in component.get_parents():
            if parent.duplicate_policy == Group.DuplicatePolicy.DENY_MULTIPLE_PARENTS:
                raise ValueError(f"Error: {parent.name} has the policy DENY_MULTIPLE_PARENTS, "
                                 "which denies adding multiple parents.")

            if parent.duplicate_policy == Group.DuplicatePolicy.ALLOW_NEW_PARENT_IF:
                if not parent.condition_func or not parent.condition_func(parent, component):
                    raise ValueError(f"Error: Condition for adding {component.name} to {parent.name} was not satisfied.")

        # Check the policy of the current group (self)
        if self.duplicate_policy == Group.DuplicatePolicy.DENY_MULTIPLE_PARENTS and component.get_parents():
            raise ValueError(f"Error: {self.name} has the policy DENY_MULTIPLE_PARENTS, "
                             "and this component already has a parent.")

        if self.duplicate_policy == Group.DuplicatePolicy.ALLOW_NEW_PARENT_IF:
            if not self.condition_func or not self.condition_func(self, component):
                raise ValueError(f"Error: Condition for adding {component.name} to {self.name} was not satisfied.")

    def _validate_remove_logic(self, component: Graphic) -> None:
        """
        Validation logic specifically for remove operation. Skips checks for multiple parents.
        """
        if component not in self.get_children():
            raise ValueError(f"Error: {component.name} is not a child of {self.name}, cannot remove.")

    def _undo_add(self, component: Graphic) -> None:
        """
        Rollback the add operation directly by updating _parents and _children.
        """
        if component in self.get_children():
            component._parents.remove(self)
            self._children.remove(component)

    def _undo_remove(self, component: Graphic) -> None:
        """
        Rollback the remove operation directly by updating _parents and _children.
        """
        component._parents.append(self)
        self._children.append(component)

    def validate_structure(self) -> None:
        """
        Validate the structure of the graphic component using class-level validation settings.
        """
        self._validator.validate_structure(**Group.validation_settings)
