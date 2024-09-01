from modules.helpers.helper import Helper

class TestFileCreator:
    def __init__(self, filename, root_module=None):
        self.filename = filename
        self.helper = Helper(filename, root_module)

    def create_test_file(self, state_name, project_structure):
        # Convert state name to snake_case for filenames and method names
        state_name_snake = self.helper.convert_to_snake_case(state_name)
        
        # Get the context name and its snake_case version
        context_name = project_structure["context"]
        context_name_snake = self.helper.convert_to_snake_case(context_name)
        
        # Get state transitions for the current state
        state_transitions = project_structure["state_transitions"]
        valid_transitions = state_transitions.get(state_name, [])

        # Write import statements for pytest, the context, and states
        self.helper.write_code_line(0, 'import pytest')
        self.helper.write_import_line(f'{context_name_snake}.{context_name_snake}', context_name)

        for state in state_transitions.keys():
            state_snake = self.helper.convert_to_snake_case(state)
            self.helper.write_import_line(f'{context_name_snake}.states.{state_snake}_state', f'{state}State')

        self.helper.write_empty_line()

        # Write test for each possible state transition
        for target_state in state_transitions.keys():
            test_name = f'test_transition_from_{state_name_snake}_to_{self.helper.convert_to_snake_case(target_state)}'
            
            self.helper.write_code_line(0, f'def {test_name}():')
            self.helper.write_code_line(1, f'{context_name_snake} = {context_name}()')
            self.helper.write_code_line(1, f'{context_name_snake}._state = {state_name}State()')
            
            if target_state == state_name:
                # Test transitioning to the same state (should return True)
                self.helper.write_code_line(1, f'result = {context_name_snake}.set_state_to_{self.helper.convert_to_snake_case(target_state)}()')
                self.helper.write_code_line(1, f'assert result is True')
                self.helper.write_code_line(1, f'assert isinstance({context_name_snake}._state, {state_name}State)')
            elif target_state in valid_transitions:
                # Test valid state transition (should return True)
                self.helper.write_code_line(1, f'result = {context_name_snake}.set_state_to_{self.helper.convert_to_snake_case(target_state)}()')
                self.helper.write_code_line(1, f'assert result is True')
                self.helper.write_code_line(1, f'assert isinstance({context_name_snake}._state, {target_state}State)')
            else:
                # Test invalid state transition (should return False)
                self.helper.write_code_line(1, f'result = {context_name_snake}.set_state_to_{self.helper.convert_to_snake_case(target_state)}()')
                self.helper.write_code_line(1, f'assert result is False')
                self.helper.write_code_line(1, f'assert isinstance({context_name_snake}._state, {state_name}State)')
            
            self.helper.write_empty_line()

        # Save the file
        self.helper.save()
