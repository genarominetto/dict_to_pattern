from abc import ABC, abstractmethod
from typing import Callable, List, Optional, Any, Dict, Union, Set
from graphic.abstract.graphic_modules.data_loader import DataLoader
from graphic.abstract.graphic_modules.graphic_validator import GraphicValidator

class Graphic(ABC):
    """
    Abstract base class for all components (both composite and leaf).
    """

    _id_counter = 0  # Class variable to keep track of the ids across all instances
    _loader = DataLoader()

    def __init__(self, name: str):
        self._parents: List['Graphic'] = []  # Now allowing multiple parents
        self._id = self._generate_id()  # Automatically assign a unique id to each instance
        self._children: List['Graphic'] = []  # Private children property
        self.name = name
        self._validator = GraphicValidator(self)  # Initialize the validator with the current component instance

    def __hash__(self):
        pass

    def __str__(self):
        pass

    @classmethod
    def _ensure_tuple(cls, args: Union[tuple, Any]) -> tuple:
        if isinstance(args, tuple):
            return args
        return (args,)

    @classmethod
    def _generate_id(cls) -> int:
        """Generates a new unique id for each instance."""
        cls._id_counter += 1
        return cls._id_counter

    def any_active(self) -> bool:
        """Dummy implementation for method any_active."""
        # Assuming that this is a method returning False for now.
        return False

    def _validate_composite_logic(self):
        pass

    def _validate_remove_logic(self):
        pass

    def validate_structure(self,
        no_circular_references: bool = True,
        no_parent_duplication_conflict: bool = True,
        parent_child_relationships_are_consistent: bool = True,
        only_component_objects_in_composites: bool = True,
        all_parents_are_composites: bool = True,
        leaf_has_no_children: bool = True,
        components_are_unique: bool = True,
        ids_are_unique: bool = True,
        names_are_unique: bool = True,
        all_composites_use_deny_policy: bool = False,
        max_one_parent: bool = True,
        condition_func_in_all_conditional_composites: bool = True
    ) -> None:
        """
        Validates the structure of the component by delegating to the Validator.
        
        Each validation can be individually toggled on or off using boolean flags.
        Setting any flag to `False` will skip that specific validation.
        
        Raises:
            ValueError: If any validation fails.
        """
        self._validator.validate_structure(
            no_circular_references=no_circular_references,
            no_parent_duplication_conflict=no_parent_duplication_conflict,
            parent_child_relationships_are_consistent=parent_child_relationships_are_consistent,
            only_component_objects_in_composites=only_component_objects_in_composites,
            all_parents_are_composites=all_parents_are_composites,
            leaf_has_no_children=leaf_has_no_children,
            components_are_unique=components_are_unique,
            ids_are_unique=ids_are_unique,
            names_are_unique=names_are_unique,
            all_composites_use_deny_policy=all_composites_use_deny_policy,
            max_one_parent=max_one_parent,
            condition_func_in_all_conditional_composites=condition_func_in_all_conditional_composites
        )

    @abstractmethod
    def add(self, component: 'Graphic') -> None:
        """Adds a child component."""
        pass

    @abstractmethod
    def remove(self, component: 'Graphic') -> None:
        """Removes a child component."""
        pass

    def is_composite(self) -> bool:
        """Returns True if this component is a composite."""
        return bool(self.get_children())

    def get_children(self) -> List['Graphic']:
        """Get the list of children for this component."""
        return self._children

    def remove_components_recursively(self) -> None:
        """Recursively remove components."""
        for child in self.get_children():
            child.remove_components_recursively()
        self._children.clear()

    def get_components_recursively(self) -> List['Graphic']:
        """Recursively gather all components."""
        components = [self]
        for child in self.get_children():
            components.extend(child.get_components_recursively())
        return components

    def execute_operation_recursively(self, operation: Callable[['Graphic'], None]) -> None:
        """Recursively execute an operation on this component and all its children."""
        operation(self)
        for child in self.get_children():
            child.execute_operation_recursively(operation)

    @abstractmethod
    def get_structure_as_dict(self) -> Dict:
        """Returns a dictionary representation of the component structure."""
        pass

    def is_leaf(self) -> bool:
        """Returns True if this component is a leaf node."""
        return not self.get_children()

    @property
    def id(self) -> int:
        return self._id

    def calculate_depth(self) -> int:
        """Calculate the depth of the component tree."""
        if not self.get_children():
            return 1
        return 1 + max(child.calculate_depth() for child in self.get_children())

    def get_parents(self) -> List['Graphic']:
        """Get the list of parents for this component."""
        return self._parents

    def clone(self) -> 'Graphic':
        """Create a step-by-step clone of this component, assigning a new ID to the clone and its children."""
        cloned_component = self.__class__.__new__(self.__class__)

        for attr_name, attr_value in self.__dict__.items():
            if attr_name == '_id':
                setattr(cloned_component, '_id', self._generate_id())
            else:
                setattr(cloned_component, attr_name, attr_value)

        cloned_component._children = []
        for child in self.get_children():
            cloned_child = child.clone()
            cloned_component.add(cloned_child)

        cloned_component._parents = []

        return cloned_component

    def _undo_add(self):
        pass

    def _undo_remove(self):
        pass

    def export_to_pickle(self, path: str) -> None:
        """Exports the component structure to a pickle file."""
        self._loader.export_to_pickle(self, path)

    @classmethod
    def import_from_pickle(cls, path: str) -> 'Graphic':
        """Imports a component structure from a pickle file."""
        return cls._loader.import_from_pickle(path)

