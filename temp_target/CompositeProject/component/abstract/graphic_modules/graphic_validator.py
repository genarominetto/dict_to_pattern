from typing import Set


class GraphicValidator:
    """
    Responsible for validating the structure of Graphic components recursively from the root.
    """

    def __init__(self, graphic):
        self.graphic = graphic

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
        """Recursively validates the structure of the graphic starting from the root."""

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
        graphic = self.graphic
        if graphic in visited:
            raise ValueError(f"Circular reference found in component {graphic.name} (id {graphic.id}).")
        visited.add(graphic)
        for child in graphic.get_children():
            child._validator._validate_no_circular_references(visited)
        visited.remove(graphic)

    def _validate_no_parent_duplication_conflict(self):
        """Validate that no component has multiple parents (duplication conflict)."""
        graphic = self.graphic
        if len(graphic.get_parents()) > 1:
            raise ValueError(f"Component {graphic.name} (id {graphic.id}) has multiple parents.")

        for child in graphic.get_children():
            child._validator._validate_no_parent_duplication_conflict()

    def _validate_parent_child_relationships(self):
        """Ensure parent-child relationships are consistent."""
        graphic = self.graphic
        for child in graphic.get_children():
            if graphic not in child.get_parents():
                raise ValueError(f"Parent-child inconsistency between {graphic.name} and {child.name}.")
            child._validator._validate_parent_child_relationships()

    def _validate_only_graphic_objects_in_groups(self):
        """Check that only graphic objects exist within groups."""
        graphic = self.graphic
        from component.abstract.graphic import Graphic
        if not all(isinstance(child, Graphic) for child in graphic.get_children()):
            raise ValueError(f"Group {graphic.name} contains non-graphic children.")
        for child in graphic.get_children():
            child._validator._validate_only_graphic_objects_in_groups()

    def _validate_all_parents_are_groups(self):
        """Ensure all parents of a component are group objects."""
        graphic = self.graphic
        for parent in graphic.get_parents():
            if not self._is_group_instance(parent):
                raise ValueError(f"Component {graphic.name} (id {graphic.id}) has a non-group parent.")
        for child in graphic.get_children():
            child._validator._validate_all_parents_are_groups()

    def _validate_leaf_has_no_children(self):
        """Ensure leaf components do not have children."""
        graphic = self.graphic
        if self._is_leaf_instance(graphic) and graphic.get_children():
            raise ValueError(f"Leaf component {graphic.name} (id {graphic.id}) has children.")
        for child in graphic.get_children():
            child._validator._validate_leaf_has_no_children()

    def _validate_components_unique(self, seen_components: Set['Graphic']):
        """Check if all components are unique."""
        graphic = self.graphic
        if graphic in seen_components:
            raise ValueError(f"Component {graphic.name} (id {graphic.id}) is not unique.")
        seen_components.add(graphic)
        for child in graphic.get_children():
            child._validator._validate_components_unique(seen_components)

    def _validate_ids_unique(self, seen_ids: Set[int]):
        """Ensure all component ids are unique."""
        graphic = self.graphic
        if graphic.id in seen_ids:
            raise ValueError(f"Duplicate id found: {graphic.id} for component {graphic.name}")
        seen_ids.add(graphic.id)
        for child in graphic.get_children():
            child._validator._validate_ids_unique(seen_ids)

    def _validate_names_unique(self, seen_names: Set[str]):
        """Ensure all component names are unique."""
        graphic = self.graphic
        if graphic.name in seen_names:
            raise ValueError(f"Duplicate name found: {graphic.name}")
        seen_names.add(graphic.name)
        for child in graphic.get_children():
            child._validator._validate_names_unique(seen_names)

    def _validate_all_groups_use_deny_policy(self):
        """Ensure all groups use the DENY_MULTIPLE_PARENTS policy."""
        graphic = self.graphic
        if self._is_group_instance(graphic) and graphic.duplicate_policy != self._get_duplicate_policy().DENY_MULTIPLE_PARENTS:
            raise ValueError(f"Group {graphic.name} does not use DENY_MULTIPLE_PARENTS policy.")
        for child in graphic.get_children():
            child._validator._validate_all_groups_use_deny_policy()

    def _validate_max_one_parent(self):
        """Ensure each component has at most one parent."""
        graphic = self.graphic
        if len(graphic.get_parents()) > 1:
            raise ValueError(f"Component {graphic.name} (id {graphic.id}) has more than one parent.")
        for child in graphic.get_children():
            child._validator._validate_max_one_parent()

    def _validate_condition_func_in_conditional_groups(self):
        """Ensure all groups with ALLOW_NEW_PARENT_IF have a condition_func defined."""
        graphic = self.graphic
        if self._is_group_instance(graphic) and graphic.duplicate_policy == self._get_duplicate_policy().ALLOW_NEW_PARENT_IF:
            if graphic.condition_func is None:
                raise ValueError(f"Group {graphic.name} (id {graphic.id}) uses ALLOW_NEW_PARENT_IF but has no condition_func defined.")
        for child in graphic.get_children():
            child._validator._validate_condition_func_in_conditional_groups()

    def _is_group_instance(self, component: 'Graphic') -> bool:
        """Helper method to dynamically check if a component is a Group."""
        from component.components.composite.group import Group
        return isinstance(component, Group)

    def _is_leaf_instance(self, component: 'Graphic') -> bool:
        """Helper method to dynamically check if a component is a Leaf."""
        from component.components.leafs.abstract.leaf import Leaf
        return isinstance(component, Leaf)

    def _get_duplicate_policy(self):
        """Helper method to dynamically import DuplicatePolicy."""
        from component.components.composite.group import Group
        return Group.DuplicatePolicy
