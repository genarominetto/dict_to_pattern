from abc import ABC
from abc import abstractmethod
from modules.helpers.component_file_builder.product.component_file import ComponentFile

class ComponentFileBuilder(ABC):
    def __init__(self, component_file_type):
        self.component_file = ComponentFile(component_file_type)

    @abstractmethod
    def write___init___method(self):
        pass

    @abstractmethod
    def write___hash___method(self):
        pass

    @abstractmethod
    def write___str___method(self):
        pass

    @abstractmethod
    def write__ensure_tuple_method(self):
        pass

    @abstractmethod
    def write__generate_id_method(self):
        pass

    @abstractmethod
    def write_any_bool_methods(self):
        pass

    @abstractmethod
    def write__validate_group_logic_method(self):
        pass

    @abstractmethod
    def write__validate_remove_logic_method(self):
        pass

    @abstractmethod
    def write_validate_structure_method(self):
        pass

    @abstractmethod
    def write_add_method(self):
        pass

    @abstractmethod
    def write_remove_method(self):
        pass

    @abstractmethod
    def write_is_composite_method(self):
        pass

    @abstractmethod
    def write_get_children_method(self):
        pass

    @abstractmethod
    def write_remove_components_recursively_method(self):
        pass

    @abstractmethod
    def write_get_components_recursively_method(self):
        pass

    @abstractmethod
    def write_execute_operation_recursively_method(self):
        pass

    @abstractmethod
    def write_get_structure_as_dict_method(self):
        pass

    @abstractmethod
    def write_is_leaf_method(self):
        pass

    @abstractmethod
    def write_id_method(self):
        pass

    @abstractmethod
    def write_calculate_depth_method(self):
        pass

    @abstractmethod
    def write_get_parents_method(self):
        pass

    @abstractmethod
    def write_clone_method(self):
        pass

    @abstractmethod
    def write__undo_add_method(self):
        pass

    @abstractmethod
    def write__undo_remove_method(self):
        pass

    @abstractmethod
    def write_export_to_pickle_method(self):
        pass

    @abstractmethod
    def write_import_from_pickle_method(self):
        pass

    def get_component_file(self):
        return self.component_file
