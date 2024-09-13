from abc import ABC, abstractmethod
from modules.helpers.helper import Helper

class ComponentFileBuilder(ABC):
    def __init__(self, filename, project_structure, root_module=None):
        self.filename = filename
        self.project_structure = project_structure
        self.root_module = root_module
        self.helper = Helper(filename, root_module)

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
        return self.helper.save()
