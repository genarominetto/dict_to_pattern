from modules.helpers.component_file_builder.builders.abstract.component_file_builder import ComponentFileBuilder
from modules.helpers.component_file_builder.product.component_file import ComponentFile

class LeafComponentFileBuilder(ComponentFileBuilder):
    def __init__(self):
        super().__init__("Leaf")
        self.component_file = ComponentFile("Leaf")

    def write___init___method(self):
        print("Doing write___init___method for Leaf")

    def write___hash___method(self):
        print("Doing write___hash___method for Leaf")

    def write___str___method(self):
        print("Doing write___str___method for Leaf")

    def write__ensure_tuple_method(self):
        print("Doing write__ensure_tuple_method for Leaf")

    def write__generate_id_method(self):
        print("Doing write__generate_id_method for Leaf")

    def write_any_bool_methods(self):
        print("Doing write_any_bool_methods for Leaf")

    def write__validate_group_logic_method(self):
        print("Doing write__validate_group_logic_method for Leaf")

    def write__validate_remove_logic_method(self):
        print("Doing write__validate_remove_logic_method for Leaf")

    def write_validate_structure_method(self):
        print("Doing write_validate_structure_method for Leaf")

    def write_add_method(self):
        print("Doing write_add_method for Leaf")

    def write_remove_method(self):
        print("Doing write_remove_method for Leaf")

    def write_is_composite_method(self):
        print("Doing write_is_composite_method for Leaf")

    def write_get_children_method(self):
        print("Doing write_get_children_method for Leaf")

    def write_remove_components_recursively_method(self):
        print("Doing write_remove_components_recursively_method for Leaf")

    def write_get_components_recursively_method(self):
        print("Doing write_get_components_recursively_method for Leaf")

    def write_execute_operation_recursively_method(self):
        print("Doing write_execute_operation_recursively_method for Leaf")

    def write_get_structure_as_dict_method(self):
        print("Doing write_get_structure_as_dict_method for Leaf")

    def write_is_leaf_method(self):
        print("Doing write_is_leaf_method for Leaf")

    def write_id_method(self):
        print("Doing write_id_method for Leaf")

    def write_calculate_depth_method(self):
        print("Doing write_calculate_depth_method for Leaf")

    def write_get_parents_method(self):
        print("Doing write_get_parents_method for Leaf")

    def write_clone_method(self):
        print("Doing write_clone_method for Leaf")

    def write__undo_add_method(self):
        print("Doing write__undo_add_method for Leaf")

    def write__undo_remove_method(self):
        print("Doing write__undo_remove_method for Leaf")

    def write_export_to_pickle_method(self):
        print("Doing write_export_to_pickle_method for Leaf")

    def write_import_from_pickle_method(self):
        print("Doing write_import_from_pickle_method for Leaf")
