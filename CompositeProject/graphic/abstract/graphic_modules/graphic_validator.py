from typing import Set

class GraphicValidator:
    """
    Responsible for validating the structure of Graphic components recursively from the root.
    """

    def __init__(self, component):
        self.component = component

    def validate_structure(self, 
        no_circular_references: bool = True,
        no_parent_duplication_conflict: bool = True,
        parent_child_relationships_are_consistent: bool = True,
        only_graphic_objects_in_groups: bool = True,
        all_parents_are_groups: bool = True,
        leaf_has_no_children: bool = True,
        components_are_unique: bool = True,
        ids_are_unique: bool = True,
        names_are_unique: bool = True,
        all_groups_use_deny_policy: bool = True,
        max_one_parent: bool = True,
        condition_func_in_all_conditional_groups: bool = True
    ):
        """Recursively validates the structure of the component starting from the root."""

        # Perform validations recursively starting from the root
        if no_circular_references:
            self._validate_no_circular_references(set())

        if no_parent_duplication_conflict:
            self._validate_no_parent_duplication_conflict()

        if parent_child_relationships_are_consistent:
            self._validate_parent_child_relationships()

        if only_graphic_objects_in_groups:
            self._validate_only_graphic_objects_in_groups()

        if all_parents_are_groups:
            self._validate_all_parents_are_groups()

        if leaf_has_no_children:
            self._validate_leaf_has_no_children()

        if components_are_unique:
            seen_components = set()
            self._validate_components_unique(seen_components)

        if ids_are_unique:
            seen_ids = set()
            self._validate_ids_unique(seen_ids)

        if names_are_unique:
            seen_names = set()
            self._validate_names_unique(seen_names)

        if all_groups_use_deny_policy:
            self._validate_all_groups_use_deny_policy()

        if max_one_parent:
            self._validate_max_one_parent()

        if condition_func_in_all_conditional_groups:
            self._validate_condition_func_in_conditional_groups()

    def _validate_no_circular_references(self, visited: Set['Graphic']):
        """Check recursively for circular references."""
        component = self.component
        if component in visited:
            raise ValueError(f"Circular reference found in component {component.name} (id {component.id}).")
        visited.add(component)
        for child in component.get_children():
            child._validator._validate_no_circular_references(visited)
        visited.remove(component)

    def _validate_no_parent_duplication_conflict(self):
        """Validate that no component has multiple parents (duplication conflict)."""
        component = self.component
        if len(component.get_parents()) > 1:
            raise ValueError(f"Component {component.name} (id {component.id}) has multiple parents.")

        for child in component.get_children():
            child._validator._validate_no_parent_duplication_conflict()

    def _validate_parent_child_relationships(self):
        """Ensure parent-child relationships are consistent."""
        component = self.component
        for child in component.get_children():
            if component not in child.get_parents():
                raise ValueError(f"Parent-child inconsistency between {component.name} and {child.name}.")
            child._validator._validate_parent_child_relationships()

    def _validate_only_graphic_objects_in_groups(self):
        """Check that only Graphic objects exist within Groups."""
        component = self.component
        from graphic.abstract.graphic import Graphic
        if not all(isinstance(child, Graphic) for child in component.get_children()):
            raise ValueError(f"Group {component.name} contains non-graphic children.")
        for child in component.get_children():
            child._validator._validate_only_graphic_objects_in_groups()

    def _validate_all_parents_are_groups(self):
        """Ensure all parents of a component are Group objects."""
        component = self.component
        for parent in component.get_parents():
            if not self._is_group_instance(parent):
                raise ValueError(f"Component {component.name} (id {component.id}) has a non-group parent.")
        for child in component.get_children():
            child._validator._validate_all_parents_are_groups()

    def _validate_leaf_has_no_children(self):
        """Ensure leaf components do not have children."""
        component = self.component
        if self._is_leaf_instance(component) and component.get_children():
            raise ValueError(f"Leaf component {component.name} (id {component.id}) has children.")
        for child in component.get_children():
            child._validator._validate_leaf_has_no_children()

    def _validate_components_unique(self, seen_components: Set['Graphic']):
        """Check if all components are unique."""
        component = self.component
        if component in seen_components:
            raise ValueError(f"Component {component.name} (id {component.id}) is not unique.")
        seen_components.add(component)
        for child in component.get_children():
            child._validator._validate_components_unique(seen_components)

    def _validate_ids_unique(self, seen_ids: Set[int]):
        """Ensure all component ids are unique."""
        component = self.component
        if component.id in seen_ids:
            raise ValueError(f"Duplicate id found: {component.id} for component {component.name}")
        seen_ids.add(component.id)
        for child in component.get_children():
            child._validator._validate_ids_unique(seen_ids)

    def _validate_names_unique(self, seen_names: Set[str]):
        """Ensure all component names are unique."""
        component = self.component
        if component.name in seen_names:
            raise ValueError(f"Duplicate name found: {component.name}")
        seen_names.add(component.name)
        for child in component.get_children():
            child._validator._validate_names_unique(seen_names)

    def _validate_all_groups_use_deny_policy(self):
        """Ensure all groups use the DENY_MULTIPLE_PARENTS policy."""
        component = self.component
        if self._is_group_instance(component) and component.duplicate_policy != self._get_duplicate_policy().DENY_MULTIPLE_PARENTS:
            raise ValueError(f"Group {component.name} does not use DENY_MULTIPLE_PARENTS policy.")
        for child in component.get_children():
            child._validator._validate_all_groups_use_deny_policy()

    def _validate_max_one_parent(self):
        """Ensure each component has at most one parent."""
        component = self.component
        if len(component.get_parents()) > 1:
            raise ValueError(f"Component {component.name} (id {component.id}) has more than one parent.")
        for child in component.get_children():
            child._validator._validate_max_one_parent()

    def _validate_condition_func_in_conditional_groups(self):
        """Ensure all groups with ALLOW_NEW_PARENT_IF have a condition_func defined."""
        component = self.component
        if self._is_group_instance(component) and component.duplicate_policy == self._get_duplicate_policy().ALLOW_NEW_PARENT_IF:
            if component.condition_func is None:
                raise ValueError(f"Group {component.name} (id {component.id}) uses ALLOW_NEW_PARENT_IF but has no condition_func defined.")
        for child in component.get_children():
            child._validator._validate_condition_func_in_conditional_groups()

    def _is_group_instance(self, component: 'Graphic') -> bool:
        """Helper method to dynamically check if a component is a Group."""
        from graphic.components.composite.group import Group
        return isinstance(component, Group)

    def _is_leaf_instance(self, component: 'Graphic') -> bool:
        """Helper method to dynamically check if a component is a Leaf."""
        from graphic.components.leaves.abstract.leaf import Leaf
        return isinstance(component, Leaf)

    def _get_duplicate_policy(self):
        """Helper method to dynamically import DuplicatePolicy."""
        from graphic.components.composite.group import Group
        return Group.DuplicatePolicy