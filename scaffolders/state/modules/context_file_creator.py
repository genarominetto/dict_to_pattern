from modules.helpers.helper import Helper

class ContextFileCreator:
    def __init__(self, filename, root_module=None):
        self.filename = filename
        self.helper = Helper(filename, root_module)

    def create_context_file(self, project_structure):
        # Extract relevant parts from project structure
        context_name = project_structure["context"]
        context_name_snake = self.helper.convert_to_snake_case(context_name)
        default_state = project_structure["default_state"]
        state_transitions = project_structure["state_transitions"]
        methods = project_structure.get("methods", [])

        # Write import statements for default and all other states
        for state_name in state_transitions.keys():
            state_name_snake = self.helper.convert_to_snake_case(state_name)
            self.helper.write_import_line(f'{context_name_snake}.states.{state_name_snake}_state', f'{state_name}State')

        # Write the class definition for the context
        self.helper.write_empty_line()
        self.helper.write_code_line(0, f'class {context_name}:')
        self.helper.write_code_line(1, 'def __init__(self):')
        self.helper.write_code_line(2, f'self._state = {default_state}State()')

        # Implement state transition methods
        for state_name in state_transitions.keys():
            transition_method = f'set_state_to_{self.helper.convert_to_snake_case(state_name)}'
            self.helper.write_code_line(1, f'def {transition_method}(self):')
            self.helper.write_code_line(2, f'self._state.{transition_method}(self)')
            self.helper.write_empty_line()

        # Implement additional methods
        for method in methods:
            self.helper.write_code_line(1, f'def {method}(self):')
            self.helper.write_code_line(2, f'self._state.{method}()')
            self.helper.write_empty_line()

        # Implement a report_status method to print the current state
        self.helper.write_code_line(1, 'def report_status(self):')
        self.helper.write_code_line(2, 'print(self._state)')
        self.helper.write_empty_line()

        # Save the file
        self.helper.save()
