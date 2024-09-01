from modules.helpers.helper import Helper

class MainFileCreator:
    def __init__(self, filename, root_module=None):
        self.filename = filename
        self.helper = Helper(filename, root_module)

    def create_main_file(self, project_structure):
        context_name = project_structure["context"]
        context_name_snake = self.helper.convert_to_snake_case(context_name)

        # Write import statement for the context
        self.helper.write_import_line(f'{context_name_snake}.{context_name_snake}', context_name)

        # Write the main function
        self.helper.write_empty_line()
        self.helper.write_code_line(0, 'if __name__ == "__main__":')
        self.helper.write_code_line(1, f'{context_name_snake} = {context_name}()  # Initial state: {project_structure["default_state"].lower()}')

        # Write state transition methods
        for state in project_structure["state_transitions"]:
            for transition in project_structure["state_transitions"][state]:
                transition_method = f'set_state_to_{self.helper.convert_to_snake_case(transition)}'
                self.helper.write_code_line(1, f'{context_name_snake}.{transition_method}()')

        # Write additional methods
        for method in project_structure["methods"]:
            self.helper.write_code_line(1, f'{context_name_snake}.{method}()')

        # Write a generic report_status method (assuming this will be implemented)
        self.helper.write_code_line(1, f'{context_name_snake}.report_status()')

        # Save the file
        self.helper.save()
