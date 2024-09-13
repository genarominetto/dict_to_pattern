from modules.helpers.component_file_builder.builders.abstract.component_file_builder import ComponentFileBuilder

class Director:
    def __init__(self, builder: ComponentFileBuilder):
        self.builder = builder

    def construct_component_file(self):
        self.builder.write___init___method()
        self.builder.write___hash___method()
        self.builder.write___str___method()
        self.builder.write__ensure_tuple_method()
        self.builder.write__generate_id_method()
        self.builder.write_any_bool_methods()
        self.builder.write__validate_composite_logic_method()
        self.builder.write__validate_remove_logic_method()
        self.builder.write_validate_structure_method()
        self.builder.write_add_method()
        self.builder.write_remove_method()
        self.builder.write_is_composite_method()
        self.builder.write_get_children_method()
        self.builder.write_remove_components_recursively_method()
        self.builder.write_get_components_recursively_method()
        self.builder.write_execute_operation_recursively_method()
        self.builder.write_get_structure_as_dict_method()
        self.builder.write_is_leaf_method()
        self.builder.write_id_method()
        self.builder.write_calculate_depth_method()
        self.builder.write_get_parents_method()
        self.builder.write_clone_method()
        self.builder.write__undo_add_method()
        self.builder.write__undo_remove_method()
        self.builder.write_export_to_pickle_method()
        self.builder.write_import_from_pickle_method()
        return self.builder.get_component_file()
