from modules.helpers.helper import Helper

class ConcreteStateFileCreator:
    def __init__(self, filename, root_module=None):
        self.filename = filename
        self.helper = Helper(filename, root_module)

    def create_concrete_state_file(self, state_name, project_structure):
        state_name_snake = self.helper.convert_to_snake_case(state_name)
        context_name = project_structure["context"]
        context_name_snake = self.helper.convert_to_snake_case(context_name)
        properties = project_structure.get("properties", [])
        methods = project_structure.get("methods", [])
        state_transitions = project_structure.get("state_transitions", {})

        # Write import statement for the base state class
        self.helper.write_import_line(f'{context_name_snake}.states.abstract.state', 'State')

        # Write class definition for the concrete state
        self.helper.write_empty_line()
        self.helper.write_code_line(0, f'class {state_name}State(State):')
        self.helper.write_code_line(1, 'def __init__(self):')
        self.helper.write_code_line(2, 'super().__init__()')
        self.helper.write_code_line(2, f'self.name = "{state_name} State"')

        # Initialize properties
        for prop in properties:
            self.helper.write_code_line(2, f'self.{prop} = None')

        self.helper.write_empty_line()

        # Define state transition methods
        all_states = state_transitions.keys()

        for target_state in all_states:
            transition_method = f'set_state_to_{self.helper.convert_to_snake_case(target_state)}'

            # Case 1: Transition to the same state (already in state)
            if state_name == target_state:
                self.helper.write_code_line(1, f'def {transition_method}(self, context):')
                self.helper.write_code_line(2, f'print(f"Already in {{self.name}}.")')
                self.helper.write_code_line(2, 'return True')
            
            # Case 2: Valid transition to another state
            elif target_state in state_transitions.get(state_name, []):
                self.helper.write_code_line(1, f'def {transition_method}(self, context):')
                self.helper.write_code_line(2, f'print(f"Switching from {{self.name}} to {target_state} state.")')
                self.helper.write_code_line(2, f'context._state = {target_state}State()')
                self.helper.write_code_line(2, 'return True')
            
            # Case 3: Invalid transition (not allowed)
            else:
                self.helper.write_code_line(1, f'def {transition_method}(self, context):')
                self.helper.write_code_line(2, f'print(f"Transition from {{self.name}} to {target_state} state is not allowed.")')
                self.helper.write_code_line(2, 'return False')

            self.helper.write_empty_line()

        # Implement additional methods
        for method in methods:
            self.helper.write_code_line(1, f'def {method}(self):')
            self.helper.write_code_line(2, 'pass')
            self.helper.write_empty_line()

        # Import other states for transitions
        for target_state in state_transitions.get(state_name, []):
            target_state_snake = self.helper.convert_to_snake_case(target_state)
            self.helper.write_import_line(f'{context_name_snake}.states.{target_state_snake}_state', f'{target_state}State')

        # Save the file
        self.helper.save()
